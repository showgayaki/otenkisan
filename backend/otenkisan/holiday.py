import json
import csv
import requests
from datetime import datetime


class Holiday:
    def __init__(self, json_dir):
        self.json_path = json_dir.joinpath('holiday.json')

    def is_updated_holiday(self, dt_now):
        """
        元日は必ず登録されているはずなので、holiday.jsonに
        「****-01-01」キーが存在するかどうかで祝日を取得済みか判定する
        """
        with open(self.json_path) as f:
            holiday_dict = json.load(f)

        new_years_day = dt_now.strftime('%Y-01-01')
        if new_years_day in holiday_dict:
            return True

        return False

    def fetch_holiday(self, holiday_url):
        holiday_dict = {}
        try:
            res = requests.get(holiday_url)
            res.encoding = res.apparent_encoding

            decoded = res.content.decode('shift-JIS')
            holiday_list = csv.reader(decoded.splitlines(), delimiter=',')

            for i, row in enumerate(holiday_list):
                # 1行目はヘッダー
                if i == 0:
                    continue

                # ['2023/1/2', '休日'] <- この形で来るので、
                # {'2023-01-02': '休日'} <- この形にする
                # いったんdatetimeオブジェクトにして、ゼロ埋め文字列に変換
                holiday_date = datetime.strptime(row[0], '%Y/%m/%d').strftime('%Y-%m-%d')
                holiday_dict[holiday_date] = row[1]

            # jsonファイルを保存
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(holiday_dict, f, indent=4, ensure_ascii=False)

            return {'level': 'info', 'detail': 'Holiday data Update is Succeded.'}
        except Exception as e:
            return {'level': 'error', 'detail': f'Holiday data Update is FAILED({e}).'}
