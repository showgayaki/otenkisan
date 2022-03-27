import requests


class Switchbot:
    def __init__(self, api_url, access_token):
        self.TIME_OUT = (3, 6)
        self.api_url = api_url
        self.headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json; charset=utf8',
        }

    def fetch_temp_data(self):
        temp_dict = {}
        try:
            res = requests.get(self.api_url, headers=self.headers, timeout=self.TIME_OUT)

            if res.status_code == 200:
                temp = res.json()['body']

                temp_dict['temperature'] = temp['temperature']
                temp_dict['humidity'] = temp['humidity']
            else:
                temp_dict['error'] = 'Status Code:{} From:{}'.format(res['status_code'], self.api_url)
        except Exception as e:
            temp_dict['error'] = str(e)

        return temp_dict
