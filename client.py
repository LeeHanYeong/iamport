import requests
from requests import adapters, Session as DefaultSession

IAMPORT_API_URL = 'https://api.iamport.kr'

API_GET_TOKEN = '/users/getToken'


class IamportResponseError(Exception):
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message


class IamportSession(DefaultSession):
    def request(self, *args, **kwargs):
        response = super().request(*args, **kwargs)
        response.raise_for_status()
        result = response.json()
        if result['code'] != 0:
            raise IamportResponseError(result.get('code'), result.get('message'))
        return result.get('response')


class Iamport:
    def __init__(self, imp_key, imp_secret, imp_url=IAMPORT_API_URL):
        self.imp_key = imp_key
        self.imp_secret = imp_secret
        self.imp_url = imp_url
        session = IamportSession()
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
        session.headers.update({'Content-Type': 'application/json'})
        self.session = session

    def _get_token(self):
        url = f'{self.imp_url}{API_GET_TOKEN}'
        params = {
            'imp_key': self.imp_key,
            'imp_secret': self.imp_secret,
        }
        response = self.session.post(url, json=params)
