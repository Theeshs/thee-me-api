from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests

# Replace these with your LinkedIn app credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = 'r_liteprofile r_emailaddress w_member_social'
LINKEDIN_USERNAME = 'YOUR_LINKEDIN_USERNAME'
LINKEDIN_PASSWORD = 'YOUR_LINKEDIN_PASSWORD'

# Set up Selenium WebDriver
options = Options()
options.headless = True  # Run in headless mode
driver = webdriver.Chrome(options=options)

try:
    # Construct the LinkedIn authorization URL
    authorization_url = (
        'https://www.linkedin.com/oauth/v2/authorization'
        '?response_type=code'
        f'&client_id={CLIENT_ID}'
        f'&redirect_uri={REDIRECT_URI}'
        f'&scope={SCOPE}'
    )

    # Navigate to the authorization URL
    driver.get(authorization_url)
    time.sleep(2)  # Allow the page to load

    # Find and fill the username field
    username_field = driver.find_element(By.ID, 'username')
    username_field.send_keys(LINKEDIN_USERNAME)

    # Find and fill the password field
    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(LINKEDIN_PASSWORD)
    password_field.send_keys(Keys.RETURN)

    time.sleep(2)  # Wait for the login to process

    # Handle potential redirects and consent screens
    if 'grant' in driver.current_url:
        grant_button = driver.find_element(By.XPATH, '//button[contains(text(), "Allow")]')
        grant_button.click()
        time.sleep(2)  # Allow for redirect

    # Extract the authorization code from the URL
    current_url = driver.current_url
    authorization_code = current_url.split('code=')[1].split('&')[0]
    print(f'Authorization Code: {authorization_code}')
finally:
    driver.quit()

# Exchange the authorization code for an access token
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
payload = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': REDIRECT_URI,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.post(token_url, data=payload, headers=headers)
if response.status_code != 200:
    raise Exception(f'Error fetching access token: {response.text}')

access_token = response.json().get('access_token')
print(f'Access Token: {access_token}')
