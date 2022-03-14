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
            'target_url': os.environ.get('TARGET_URL'),
            'target_attr': os.environ.get('TARGET_ATTR'),
        }
        return conf
