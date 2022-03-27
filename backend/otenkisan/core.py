import json
import socket
from datetime import datetime
from pathlib import Path
from config import Config
from weather_forecast import WeatherForecast
from switchbot import Switchbot
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
    # とりあえずFalse入れておく
    forecast_data['none_last_max'] = False
    forecast_data['none_last_min'] = False

    # 今回取得分がNoneの場合は前回データ引き継ぎ
    if current['max'] is None:
        forecast_data['max'] = last['max']
        forecast_data['none_last_max'] = True
    elif last['none_last_max'] is True:
        # 前回Noneで今回値が取れていれば(日をまたいだら)min_max更新
        min_max['max'] = last['max']

    # 今回取得分がNoneの場合は前回データ引き継ぎ
    if current['min'] is None:
        forecast_data['min'] = last['min']
        forecast_data['none_last_min'] = True
    elif last['none_last_min'] is True:
        # 前回Noneで今回値が取れていれば(日をまたいだら)min_max更新
        min_max['min'] = last['min']

    # 気温の前日比計算
    max_diff = int(forecast_data['max']) - int(min_max['max'])
    min_diff = int(forecast_data['min']) - int(min_max['min'])
    # 0の場合はプラマイ表記に置き換える
    forecast_data['max_diff'] = '[{:+}]'.format(max_diff).replace('+', '±') if max_diff == 0 else '[{:+}]'.format(max_diff)
    forecast_data['min_diff'] = '[{:+}]'.format(min_diff).replace('+', '±') if min_diff == 0 else '[{:+}]'.format(min_diff)
    # パーセント表示ない時用
    forecast_data['rainy_percent'] = [percent.replace('--%', '---') for percent in forecast_data['rainy_percent']]

    return min_max, forecast_data


def save_json(json_path, data):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def fetch_forecast(**kwargs):
    # 天気予報開始
    kwargs['log'].logging('info', 'Start to fetch Weather Forecast.')
    kwargs['log'].logging('info', 'Forecast API URL: {}'.format(kwargs['cfg']['forecast_api_url']))
    # 天気予報取得
    wf = WeatherForecast(kwargs['cfg']['forecast_api_url'])
    forecast = wf.fetch_weather_forecast()
    kwargs['log'].logging('info', 'Forecast: {}'.format(forecast))
    # アイコンダウンロード
    forecast_icon = wf.fetch_forecast_icon(kwargs['root_dir'], forecast['icon'])
    forecast_path = Path(kwargs['json_dir']).joinpath('forecast.json')
    temp_yesterday_path = Path(kwargs['json_dir']).joinpath('temp_yesterday.json')

    # 戻ってきたdictにエラーなかったらjsonとして保存
    if 'error' in forecast:
        kwargs['log'].logging('error', 'FAILED to fetch Weather Forecast.')
    else:
        kwargs['log'].logging('info', 'Succeeded to fetch Weather Forecast.')
        last_forecast = load_json(forecast_path)
        last_min_max = load_json(temp_yesterday_path)
        kwargs['log'].logging('info', 'last_forecast: {}'.format(last_forecast))
        kwargs['log'].logging('info', 'last_min_max: {}'.format(last_min_max))

        # アイコンURLをローカルのパスに変更
        if forecast_icon:
            kwargs['log'].logging('info', 'Save forecast icon => [{}]'.format(forecast_icon))
            forecast['icon'] = forecast_icon.split('public/')[-1]
        else:
            kwargs['log'].logging('error', 'FAILED to fetch forecast icon.')
            forecast['icon'] = 'favicon.ico'

        # 保存用json組み立て
        min_max, forecast_data = build_json_data(last_forecast, forecast, last_min_max)

        # 最高最低が更新されていればjson保存
        if load_json(temp_yesterday_path) != min_max:
            kwargs['log'].logging('info', 'Update min_max')
            save_json(temp_yesterday_path, min_max)

        kwargs['log'].logging('info', 'min_max: {}'.format(min_max))
        kwargs['log'].logging('info', 'Current forecast_data: {}'.format(forecast_data))
        # 予報json保存
        save_json(forecast_path, forecast_data)
        kwargs['log'].logging('info', '=== Finished to fetch forecast. ===')


def fetch_switchbot_data(**kwargs):
    # 開始ログ
    kwargs['log'].logging('info', 'Start to fetch Switchbot data.')
    kwargs['log'].logging('info', 'Switchbot API URL: {}'.format(kwargs['cfg']['switchbot_api_url']))
    # Switchbotからデータ取得
    sb = Switchbot(kwargs['cfg']['switchbot_api_url'], kwargs['cfg']['switchbot_access_token'])
    temp_data = sb.fetch_temp_data()
    kwargs['log'].logging('info', 'Switchbot data: {}'.format(temp_data))
    # jsonに保存
    switchbot_path = Path(kwargs['json_dir']).joinpath('switchbot.json')
    kwargs['log'].logging('info', 'Switchbot data save to {}'.format(switchbot_path))
    save_json(switchbot_path, temp_data)
    kwargs['log'].logging('info', '=== Finished to fetch Switchbot. ===')


def main():
    computer_name = socket.gethostname() # 実行コンピュータ名
    root_dir = Path(__file__).resolve().parents[1] # backendプロジェクトルート
    dt_now = datetime.now() # 現在時刻取得
    now_minutes = dt_now.strftime('%M') # 現在分数取得
    json_dir = Path(root_dir.parent).joinpath('public/json') # json保存先
    if not json_dir.is_dir(): Path.mkdir(json_dir) # jsonフォルダ無かったら作成
    cfg = load_config(root_dir) # 設定読み込み

    # ログ開始
    log = Logger(root_dir)
    log.logging('info', '===== {} Started on {} ====='.format(cfg['app_name'], computer_name))

    # 指定分数なら天気予報取得
    if cfg['forecast_acquisition_minute'] == now_minutes:
        fetch_forecast(**vars())

    # switchbotのAPI URLが設定されていたら実行
    if cfg['switchbot_api_url']:
        fetch_switchbot_data(**vars())

    log.logging('info', '===== {} Stopped. ====='.format(cfg['app_name']))


if __name__ == '__main__':
    main()
