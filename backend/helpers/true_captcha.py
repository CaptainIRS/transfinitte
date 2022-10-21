import requests
import base64
import os

from dotenv import load_dotenv


async def solve_captcha():
    load_dotenv()
    user_id = os.getenv('TRUECAPTCHA_USER_ID')
    api_key = os.getenv('TRUECAPTCHA_API_KEY')

    session = requests.Session()
    image = session.get(
        'https://electoralsearch.in/Home/GetCaptcha?image=true').content
    # bytes to base64
    image = base64.b64encode(image).decode('utf-8')

    # bytes to base64
    cookies = session.cookies.get_dict()

    result = requests.post('https://api.apitruecaptcha.org/one/gettext', json={
        "userid": user_id,
        "apikey": api_key,
        "data": image,
        "case": "mixed",
    }
    )
    with open(f'capcha/captcha-{result.json()["result"]}.png', 'wb') as f:
        f.write(base64.b64decode(image))
    return (result.json()['result'], cookies)

if __name__ == '__main__':
    print(solve_captcha())
