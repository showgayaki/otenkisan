import requests
from pathlib import Path


class WeatherForecast:
    """
    {
        "state": "晴れ",
        "max": "13℃",
        "min": "5℃",
        "max_diff": "[-5]",
        "min_diff": "[0]",
        "icon": "https://s.yimg.jp/images/weather/general/next/size150/100_night.png",
        "rainy-percent": [
            "---",
            "---",
            "---",
            "0%"
        ]
    }
    """
    def __init__(self, api_url):
        self.TIME_OUT = (3, 6)
        self.USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
        self.api_url = api_url

    def fetch_weather_forecast(self):
        forecast_dict = {}
        try:
            res = requests.get(self.api_url, headers=self.USER_AGENT, timeout=self.TIME_OUT)
            if res.status_code == 200:
                forecast = res.json()['forecasts'][0]

                forecast_dict['state'] = forecast['telop']
                forecast_dict['max'] = forecast['temperature']['max']['celsius']
                forecast_dict['max_diff'] = ''
                forecast_dict['min'] = forecast['temperature']['min']['celsius']
                forecast_dict['min_diff'] = ''
                forecast_dict['icon'] = forecast['image']['url']
                forecast_dict['rainy_percent'] = [percent for percent in forecast['chanceOfRain'].values()]
            else:
                forecast_dict['error'] = 'Status Code:{} From:{}'.format(res.status_code, self.api_url)
        except Exception as e:
            forecast_dict['error'] = str(e)

        return forecast_dict

    def fetch_forecast_icon(self, root_dir, src_url):
        file_name = src_url.split('/')[-1]
        image_dir = Path(root_dir.parent).joinpath('public/images')
        image_file_path = Path(image_dir).joinpath(file_name)
        try:
            res = requests.get(src_url, headers=self.USER_AGENT, timeout=self.TIME_OUT)
            image = res.content
            # imagesフォルダなかったら作成
            if not image_dir.is_dir(): Path.mkdir(image_dir)
            # 画像保存
            with open(image_file_path, 'wb') as f:
                f.write(image)

            # 画像ファイルのフルパスを返す
            if Path(image_file_path).exists():
                return str(image_file_path)
            else:
                return False
        except Exception as e:
            return str(e)
