import json
from pathlib import Path
from config import Config
from weather_forecast import WeatherForecast
from logger import Logger


def load_config(root_dir):
    config = Config(root_dir)
    cfg = config.fetch_config()
    return cfg


def load_json(json_path):
    last_dict = {}
    try:
        last_dict = json.load(open(json_path))
    except Exception as e:
        last_dict['error'] = str(e)

    return last_dict


def save_json(json_path, data):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    root_dir = Path(__file__).resolve().parents[1]
    # ログ
    log = Logger(root_dir)
    # 設定読み込み
    cfg = load_config(root_dir)
    # 天気予報取得
    wf = WeatherForecast(cfg['target_url'], cfg['target_attr'])
    forecsast = wf.fetch_weather_forecast()

    json_dir = Path(root_dir.parent).joinpath('public/json')
    # jsonフォルダ無かったら作成
    if not json_dir.is_dir(): Path.mkdir(json_dir)
    # json保存
    save_json(Path(json_dir).joinpath('temp.json'), forecsast)


if __name__ == '__main__':
    main()
