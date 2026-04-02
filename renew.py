import requests
import os
import sys
from bs4 import BeautifulSoup

def renew_account(username, password):
    session = requests.Session()
    login_url = 'https://www.pythonanywhere.com/login/'
    
    # 1. Get CSRF Token
    r = session.get(login_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    print('user: '+str(username)+' pass: '+str(password))
    # 2. Log In
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token,
        'login_view-current_step': 'auth'
    }
    r = session.post(login_url, data=login_data, headers={'Referer': login_url})
    
    if 'Log out' not in r.text:
        print(f"FAILED: Login failed for {username}. Check your USER_N and PASS_N secrets.")
        return False
    
    # 3. Hit the Extend Button
    # Note: Referer header is often required by PA to prevent CSRF errors
    extend_url = f'https://www.pythonanywhere.com/user/{username}/webapp/extend'
    headers = {'Referer': f'https://www.pythonanywhere.com/user/{username}/webapps/'}
    r = session.post(extend_url, data={'csrfmiddlewaretoken': csrf_token}, headers=headers)
    
    if r.status_code == 200:
        print(f"SUCCESS: Extended {username} until next month!")
        return True
    else:
        print(f"ERROR: Failed to extend {username}. Status: {r.status_code}")
        return False

if __name__ == "__main__":
    user = os.getenv('PA_USERNAME')
    pw = os.getenv('PA_PASSWORD')
    if not user or not pw:
        print("Missing environment variables PA_USERNAME or PA_PASSWORD")
        sys.exit(1)
    
    success = renew_account(user, pw)
    if not success:
        sys.exit(1)
