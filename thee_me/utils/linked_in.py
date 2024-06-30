import requests


class BasePlatformRunner:
    def __init__(self, url, auth_creds):
        self.url = url
        self.auth_creds = auth_creds

    def get_auth_token(self, token):
        raise