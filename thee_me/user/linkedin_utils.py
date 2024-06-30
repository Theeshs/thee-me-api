from thee_me.enums.api_url_enums import LinkedInAPIUrls
import requests
from thee_me.exceptions.linkedin_api_exceptions import *


def linkedin_access_token(auth_code):
    """ calling the linked in API and will get the auth tokens and returns it. do we need a class for this?
    """
    if not auth_code:
        raise Exception("Auth code is required")

    creds = {
        "client_id": "86cu5r0eryy02u",
        "client_secret": "WPL_AP0.Um84f0ou5JKS6HEX.NzEyNzk4MzEz",
        "grant_type": "authorization_code",
        "redirect_uri": "https://oauth.pstmn.io/v1/callback",
        "code": auth_code
    }

    try:
        response = requests.post(
            f"{LinkedInAPIUrls.LINKEDIN_BASE_API.value}{LinkedInAPIUrls.AUTH_API.value}", data=creds)
        print(response)
        if response.status_code in [400, 401]:
            raise LinkedInAPIException(response.text)

        """
        should save to the database here, save only the refresh token and save how long it will valid. So we can
        show the user the time left for the token to expire.
        """
        return response.json()
    except Exception as e:
        raise LinkedInAuthenticationException("86cu5r0eryy02u")


def get_access_token_with_refresh_token(db):
    creds = {}

    try:
        raise NotImplemented("Functionality not implemented yet")
    except Exception as e:
        raise LinkedInAuthenticationException(str(e))