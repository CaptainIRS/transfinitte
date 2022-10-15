import requests
import base64
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from family_tree import get_family_tree

from models import Cookies
from pdf2image import convert_from_bytes
from chop import chop_image
from parser import parse_text
from multiprocessing import Pool, cpu_count

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=[
                   'http://localhost:3000'], allow_methods=['*'], allow_headers=['*'])

app.get('/')


def get_url(state_no, dist_no, ac_no, part_no):
    return f'https://www.elections.tn.gov.in/SSR2022_MR_05012022/dt{dist_no}/ac{ac_no.zfill(3)}/ac{ac_no.zfill(3)}{part_no.zfill(3)}.pdf'


async def root():
    return {'message': 'Hello World'}


@app.get('/state_list')
async def get_state_list():
    url = 'https://electoralsearch.in/home/getstatelist'
    response = requests.get(url)
    return response.json()


@app.get('/district_list')
async def get_district_list(state_no):
    url = f'https://electoralsearch.in/home/getdistlist?st_code={state_no}'
    response = requests.get(url)
    return response.json()


@app.get('/assembly_list')
async def get_assembly_list(state_no, dist_no):
    url = f'https://electoralsearch.in/home/getaclist?st_code={state_no}&dist_no={dist_no}'
    response = requests.get(url)
    return response.json()


@app.get('/captcha')
async def captcha():
    session = requests.Session()
    image = session.get(
        'https://electoralsearch.in/Home/GetCaptcha?image=true').content
    # bytes to base64
    image = base64.b64encode(image).decode('utf-8')
    return {'image': image, 'cookies': session.cookies.get_dict()}


@app.post('/tree')
async def get_tree(name, relative_name, dob, state, gender=None, district=None, ac=None):
    if district is None:
        district = ''
    if ac is None:
        ac = ''
    cookies = {
        "cookiesession1": "678B2867C4B5B295E9638138BA689FDA",
        "electoralSearchId": "2ty5kzfwrzcehfj0zxanklmr",
        "Electoral": "456c656374726f6c7365617263682d73657276657231"
    }
    if district == 'null':
        district = ''
    if ac == 'null':
        ac = ''
    location = f'{state},{district},{ac}'

    r = requests.post('https://electoralsearch.in/Home/searchVoter', data={
        'dob': dob,
        'gender': gender,  # M/F/O
        'location': location,
        'location_range': 20,
        'name': name,
        'page_no': '1',
        'results_per_page': '10',
        'reureureired': 'ca3ac2c8-4676-48eb-9129-4cdce3adf6ea',
        'rln_name': relative_name,
        'search_type': 'details',
        'txtCaptcha': 'nFaawA',
    }, cookies=cookies)
    print(r.text)
    try:
        results = r.json()['response']['docs']
    except Exception as e:
        print(e)
        return {'error': 'Invalid captcha'}
    if len(results) == 1:
        target = results[0]
        url = get_url(target['st_code'], target['dist_no'],
                      target['ac_no'], target['part_no'])
        dicts = []

        pdf = requests.get(url).content
        pages = convert_from_bytes(pdf, 500)
        with Pool(cpu_count//2) as p:
            texts = p.starmap([(pages[i], i + 1) for i in range(2, len(pages) - 1)])
        for (page_no, image_no, col, text) in texts:
            dic = parse_text(text)
            dicts.append(dic)
        return get_family_tree(target, dicts)

    elif len(results) == 0:
        return {'error': 'No results'}
    else:
        return {'error': 'Multiple results'}
