from thee_me.enums.api_url_enums import LinkedInAPIUrls
import requests
from linkedin_api.clients.auth.client import AuthClient


class LinkedInAPI:

    @staticmethod
    def auth_api(creds, url):
        try:
            print(creds)
            print(url)
            response = requests.post(url, data=creds)
            print(response)
            if response.status_code in [400, 401]:
                print(response.text)
            return response.json().get('access_token')
        except Exception as e:
            print("error")
            print(e)
            return None


    @staticmethod
    def auth_code_api(creds, url):
        pass


    @staticmethod
    def get_user_account_data(url, token):
        pass


if __name__ == '__main__':
    creds = {
        "client_id": "86cu5r0eryy02u",
        "client_secret": "WPL_AP0.Um84f0ou5JKS6HEX.NzEyNzk4MzEz",
        "grant_type": "authorization_code",
        "redirect_uri": "https://oauth.pstmn.io/v1/callback",
        "code": "AQRNkSdBED3Nw-wAbd4elup1FLhUVOpahwN1mvZR38xuGW_F9qfmKZ-o8aW7TjVwrCYfW4ltr01ECEi91St-0c4vU6BINXy13IfLca-EQXpaV6ItIktUUf4MzEWVWchholm3eHg89_T4JyVTrH-eGCPeXcZ4jEP16E3Cxnfu461ZZmxZsdB7B5o44P076XpWQiXFDqYwMG6hEzFTJ1U"
    }


    data = LinkedInAPI.auth_api(creds, f"{LinkedInAPIUrls.LINKEDIN_BASE_API.value}{LinkedInAPIUrls.AUTH_API.value}")
    # data = LinkedInAPI.get_auth(creds)
    print(data)