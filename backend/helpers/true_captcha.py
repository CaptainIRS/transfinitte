import requests
import base64

async def solve_captcha():
    session = requests.Session()
    image = session.get(
        'https://electoralsearch.in/Home/GetCaptcha?image=true').content
    # bytes to base64
    image = base64.b64encode(image).decode('utf-8')
    
    # bytes to base64
    cookies = session.cookies.get_dict()
    
    result = requests.post('https://api.apitruecaptcha.org/one/gettext', json={
        "userid":"indreshp135@gmail.com",
        "apikey":"Ef1pExkDMkiZDTtpTc5t",
        "data":image,
        "case":"mixed",
    }
    )
    with open(f'capcha/captcha-{result.json()["result"]}.png', 'wb') as f:
        f.write(base64.b64decode(image))
    return (result.json()['result'], cookies)

if __name__ == '__main__':
    print(solve_captcha())
