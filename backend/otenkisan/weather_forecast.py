import requests
from bs4 import BeautifulSoup


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
    def __init__(self, target_url, target_attr):
        self.target_url = target_url
        self.target_attr = target_attr

    def fetch_weather_forecast(self):
        forecast_dict = {}
        try:
            res = requests.get(self.target_url, timeout=(3, 6))
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, 'html.parser')
                today_weather = soup.select(self.target_attr)

                for elem in today_weather:
                    forecast_dict['state'] = elem.select_one('.weather-telop').getText()
                    forecast_dict['max'] = elem.select_one('.high-temp.temp .value').getText()
                    forecast_dict['max_diff'] = elem.select_one('.high-temp.tempdiff').getText()
                    forecast_dict['min'] = elem.select_one('.low-temp.temp .value').getText()
                    forecast_dict['min_diff'] = elem.select_one('.low-temp.tempdiff').getText()
                    forecast_dict['icon'] = elem.select_one('.weather-icon img').get('src')
                    forecast_dict['rainy_percent'] = [percent.getText() for percent in elem.select('.rain-probability td')]
            else:
                forecast_dict['error'] = 'Status Code:{} From:{}'.format(res.status_code, self.target_url)
        except Exception as e:
            forecast_dict['error'] = str(e)

        return forecast_dict
