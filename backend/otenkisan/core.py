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


def save_image():
    return False


def save_json(json_path, data):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    computer_name = socket.gethostname() # 実行コンピュータ名
    root_dir = Path(__file__).resolve().parents[1] # backendプロジェクトルート
    json_dir = Path(root_dir.parent).joinpath('public/json') # json保存先
    # 設定読み込み
    cfg = load_config(root_dir)
    # ログ
    log = Logger(root_dir)
    log.logging('info', '===== {} Started on {} ====='.format(cfg['app_name'], computer_name))
    # 天気予報取得
    log.logging('info', 'Start to fetch Weather Forecast.')
    log.logging('info', 'target_url: {}, target_attr: {}'.format(cfg['target_url'], cfg['target_attr']))
    wf = WeatherForecast(cfg['target_url'], cfg['target_attr'])
    forecast = wf.fetch_weather_forecast()
    forecast_icon = wf.fetch_forecast_icon(root_dir, forecast['icon'])

    # jsonフォルダ無かったら作成
    if not json_dir.is_dir(): Path.mkdir(json_dir)

    # 戻ってきたdictにエラーなかったらjsonとして保存
    if 'Error' in forecast:
        log.logging('error', 'FAILED to fetch Weather Forecast.')
    else:
        log.logging('info', 'Succeed to fetch Weather Forecast.')
        if forecast_icon:
            log.logging('info', 'Save forecast icon => [{}]'.format(forecast_icon))
            forecast['icon'] = forecast_icon.split('public/')[-1]
        else:
            log.logging('error', 'FAILED to fetch forecast icon.')
            forecast['icon'] = 'favicon.ico'
        # json保存
        save_json(Path(json_dir).joinpath('temp.json'), forecast)

    log.logging('info', '===== {} Stopped. ====='.format(cfg['app_name']))


if __name__ == '__main__':
    main()
