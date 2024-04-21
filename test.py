import requests

def get_csrf_cookie(url):
    response = requests.get(url)
    for cookie in response.headers.get('Set-Cookie').split(';'):
        if '_csrf=' in cookie:
            csrf_cookie = cookie.split('=')[1]
            return csrf_cookie
    return None

# Example usage
url = "https://lk.etu.ru/oauth/authorize?response_type=code&redirect_uri=https%3A%2F%2Fdigital.etu.ru%2Fattendance%2Fapi%2Fauth%2Fredirect&client_id=29"
csrf_cookie = get_csrf_cookie(url)
print(f"CSRF cookie: {csrf_cookie}")