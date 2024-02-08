import os
from dotenv import load_dotenv
from pathlib import Path


class Config:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def fetch_config(self):
        dotenv_path = Path(self.root_dir).parents[0].resolve().joinpath('.env.local')
        load_dotenv(dotenv_path)
        conf = {
            'app_name': 'otenkisan',
            'forecast_api_url': os.getenv('FORECAST_API_URL'),
            'forecast_acquisition_minute': os.getenv('FORECAST_ACQUISITION_MINUTE'),
            'switchbot_api_url': os.getenv('SWITCHBOT_API_URL'),
            'switchbot_access_token': os.getenv('SWITCHBOT_ACCESS_TOKEN'),
            'holiday_url': os.getenv('HOLIDAY_URL'),
        }
        return conf
