import json
import socket
from pathlib import Path
from config import Config
from weather_forecast import WeatherForecast
from logger import Logger


def load_config(root_dir):
    config = Config(root_dir)
    cfg = config.fetch_config()
    return cfg


def load_json(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    return json_data


def build_json_data(last, current, last_min_max):
    # とりあえず今回取得したやつ入れておく
    forecast_data = current.copy()
    # とりあえず前回のmin_max入れておく
    min_max = {'max': last_min_max['max'], 'min': last_min_max['min']}

    # 今回取得分がNoneの場合は前回データ引き継ぎ
    if current['max'] is None:
        forecast_data['max'] = last['max']
        forecast_data['none_last_max'] = True
    elif last['none_last_max'] is True:
        # 前回Noneで今回値が取れていれば(日をまたいだら)min_max更新
        min_max['max'] = last['max']
        forecast_data['none_last_max'] = False

    # 今回取得分がNoneの場合は前回データ引き継ぎ
    if current['min'] is None:
        forecast_data['min'] = last['min']
        forecast_data['none_last_min'] = True
    elif last['none_last_min'] is True:
        # 前回Noneで今回値が取れていれば(日をまたいだら)min_max更新
        min_max['min'] = last['min']
        forecast_data['none_last_min'] = False

    # 気温の前日比計算
    max_diff = int(forecast_data['max']) - int(min_max['max'])
    min_diff = int(forecast_data['min']) - int(min_max['min'])
    # 0の場合はプラマイ表記に置き換える
    forecast_data['max_diff'] = '[{:+}]'.format(max_diff).replace('+', '±') if max_diff == 0 else '[{:+}]'.format(max_diff)
    forecast_data['min_diff'] = '[{:+}]'.format(min_diff).replace('+', '±') if min_diff == 0 else '[{:+}]'.format(min_diff)

    return min_max, forecast_data


def save_json(json_path, data):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    computer_name = socket.gethostname() # 実行コンピュータ名
    root_dir = Path(__file__).resolve().parents[1] # backendプロジェクトルート
    json_dir = Path(root_dir.parent).joinpath('public/json') # json保存先
    # 設定読み込み
    cfg = load_config(root_dir)
    # ログ開始
    log = Logger(root_dir)
    log.logging('info', '===== {} Started on {} ====='.format(cfg['app_name'], computer_name))
    # 天気予報
    log.logging('info', 'Start to fetch Weather Forecast.')
    log.logging('info', 'api_url: {}'.format(cfg['api_url']))
    # 天気予報取得
    wf = WeatherForecast(cfg['api_url'])
    forecast = wf.fetch_weather_forecast()
    log.logging('info', 'Forecast: {}'.format(forecast))
    # アイコンダウンロード
    forecast_icon = wf.fetch_forecast_icon(root_dir, forecast['icon'])
    # jsonフォルダ無かったら作成
    if not json_dir.is_dir(): Path.mkdir(json_dir)
    forecast_path = Path(json_dir).joinpath('forecast.json')
    temp_yesterday_path = Path(json_dir).joinpath('temp_yesterday.json')

    # 戻ってきたdictにエラーなかったらjsonとして保存
    if 'error' in forecast:
        log.logging('error', 'FAILED to fetch Weather Forecast.')
    else:
        log.logging('info', 'Succeeded to fetch Weather Forecast.')
        last_forecast = load_json(forecast_path)
        last_min_max = load_json(temp_yesterday_path)
        log.logging('info', 'last_forecast: {}'.format(last_forecast))
        log.logging('info', 'last_min_max: {}'.format(last_min_max))

        # アイコンURLをローカルのパスに変更
        if forecast_icon:
            log.logging('info', 'Save forecast icon => [{}]'.format(forecast_icon))
            forecast['icon'] = forecast_icon.split('public/')[-1]
        else:
            log.logging('error', 'FAILED to fetch forecast icon.')
            forecast['icon'] = 'favicon.ico'

        # 保存用json組み立て
        min_max, forecast_data = build_json_data(last_forecast, forecast, last_min_max)
        log.logging('info', 'min_max: {}'.format(min_max))
        log.logging('info', 'forecast_data: {}'.format(forecast_data))

        # 最高最低が更新されていればjson保存
        if load_json(temp_yesterday_path) != min_max:
            save_json(temp_yesterday_path, min_max)
        # 予報json保存
        save_json(forecast_path, forecast_data)

    log.logging('info', '===== {} Stopped. ====='.format(cfg['app_name']))


if __name__ == '__main__':
    main()
