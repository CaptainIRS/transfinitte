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
async def get_tree(name, relative_name, dob, captcha, state, cookies: Cookies, gender=None, district=None, ac=None):
    if district is None:
        district = ''
    if ac is None:
        ac = ''
    cookies = cookies.__dict__
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
        'txtCaptcha': captcha,
    }, cookies=cookies)
    print(r.text)
    results = r.json()['response']['docs']
    if len(results) == 1:
        result = results[0]
        url = get_url(result['st_code'], result['dist_no'],
                      result['ac_no'], result['part_no'])
        # TODO: get pdf and extract dict, neo4j
        dicts = []
        pdf = requests.get(url).content
        pages = convert_from_bytes(pdf)
        for i in range(len(pages)):
            tuples = chop_image(pages[i], i)
            for tup in tuples:
                dic = parse_text(tup[3], "Tamil")
                dicts.append(dic)

        return get_family_tree(dicts)
                
    elif len(results) == 0:
        return {'error': 'No results'}
    else:
        return {'error': 'Multiple results'}
