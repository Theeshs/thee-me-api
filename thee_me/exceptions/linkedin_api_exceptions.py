class LinkedInAuthenticationException(Exception):

    def __init__(self, app_id: str):
        super().__init__(f"Linkedin authentication failed for app_id: {app_id}")


class LinkedInAPIException(Exception):

    def __init__(self, message: str):
        super().__init__(f"Linkedin API failed with error: {message}")