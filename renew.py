import requests
import os
import sys
from bs4 import BeautifulSoup

def renew_account(username, password):
    session = requests.Session()
    # Use a real browser User-Agent to avoid being blocked as a bot
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    login_url = 'https://www.pythonanywhere.com/login/'
    
    # 1. INITIAL GET: Grab the first CSRF token and cookies
    r = session.get(login_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    # 2. THE LOGIN POST: PythonAnywhere needs these specific fields
    login_data = {
        'csrfmiddlewaretoken': csrf_token,
        'auth-username': username,
        'auth-password': password,
        'login_view-current_step': 'auth' # This is the "magic" field for 2026
    }
    
    # We must send the Referer header or it will fail CSRF checks
    r = session.post(login_url, data=login_data, headers={'Referer': login_url})
    
    # DEBUG: Check if we actually logged in
    if 'Log out' not in r.text:
        print(f"FAILED: Login failed for {username}.")
        # To help you debug, let's see what the page said instead
        if "reCAPTCHA" in r.text:
            print("REASON: PythonAnywhere is asking for a CAPTCHA. You need to log in manually in a browser once.")
        return False
    
    # 3. THE EXTEND POST
    extend_url = f'https://www.pythonanywhere.com/user/{username}/webapp/extend'
    # We need the NEW CSRF token from the logged-in session
    soup = BeautifulSoup(r.text, 'html.parser')
    new_csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    r = session.post(extend_url, data={'csrfmiddlewaretoken': new_csrf}, headers={'Referer': f'https://www.pythonanywhere.com/user/{username}/webapps/'})
    
    if r.status_code == 200:
        print(f"SUCCESS: Extended {username}!")
        return True
    else:
        print(f"ERROR: Failed to extend. Status: {r.status_code}")
        return False
