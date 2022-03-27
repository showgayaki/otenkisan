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
            'forecast_api_url': os.environ.get('FORECAST_API_URL'),
            'forecast_acquisition_minute': os.environ.get('FORECAST_ACQUISITION_MINUTE'),
            'switchbot_api_url': os.environ.get('SWITCHBOT_API_URL'),
            'switchbot_access_token': os.environ.get('SWITCHBOT_ACCESS_TOKEN'),
        }
        return conf
