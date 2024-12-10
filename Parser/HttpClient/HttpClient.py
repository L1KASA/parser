import requests

class HttpClient:
    def __init__(self, url=None, cookies=None, headers=None):
        self.url = url
        self.cookies = cookies or {}
        self.headers = headers or {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0'
        }

    def get(self, url, params=None):
        response = requests.get(url, cookies=self.cookies, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Request failed with status {response.status_code}: {response.reason}")