import requests
import json
import base64

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from helpers.family_tree_v2 import get_family_tree, get_family_trees

from pdf2image import convert_from_bytes
from helpers.chop import chop_image
from helpers.parser import parse_text
from multiprocessing import Pool, cpu_count
import os

from helpers.true_captcha import solve_captcha

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=[
    '*'], allow_methods=['*'], allow_headers=['*'])

app.get('/')


def get_url(state_no, dist_no, ac_no, part_no):

    # if state_no == 'S11': # Impossible ## Andhra Pradesh
    #     return f'https://ceoaperolls.ap.gov.in/AP_Eroll_2022/Popuppage?partNumber={part_no}&roll=EnglishMotherRoll&districtName=DIST_{dist_no:02}&acname={ac_no}&acnameeng=A{ac_no}&acno={ac_no}&acnameurdu=001'
    
    # if state_no == 'S02': ## Arunachal Pradesh
    #     return 'Local URl'

    # if state_no == 'S03': ## Assam
    #     return f'http://103.8.249.227:8080/voterlist/pdfroll/D{dist_no}/A{ac_no}/MotherRoll/S03A{ac_no}P{part_no}.pdf'

    # if state_no == 'S04': ## Bihar ## Not possible

    if state_no == 'S26': ## Chhattisgarh
        return f'https://election.cg.nic.in/voterlist/pdf2022/MotherRoll/AC_{ac_no:03}/S26A{ac_no}P{part_no}.pdf'

    if state_no == 'S06': ## Gujarat
        return f'https://erms.gujarat.gov.in/ceo-gujarat/DRAFT2022/{ac_no:03}/S06A{ac_no}P{part_no}.pdf'

    if state_no == 'S07': ## Haryana
        return f'https://ceoharyana.gov.in/Finalroll2022/CMB{ac_no}/CMB{ac_no:03}{part_no:04}.PDF'

    # if state_no == 'S08': ## Himachal Pradesh ## Not possible

    if state_no == 'S10': ## Karnataka
        return f'https://ceo.karnataka.gov.in/finalroll_2022/Kannada/MR/AC{ac_no:03}/S10A{ac_no}P{part_no}.pdf'

    # if state_no == 'S11': ## Kerala ## Not possible

    # if state_no == 'S12': ## Madhya Pradesh ## Not possible

    # if state_no == 'S13': ## Maharashtra ## Not possible

    if state_no == 'S14': ## Manipur
        return f'https://ceomanipur.nic.in/eroll_manipur/Final Service Electoral Roll-2022/S14AC{ac_no:03}SRVC.pdf'

    if state_no == 'S15': ## Meghalaya
        return f'https://ceomeghalaya.nic.in/erolls/pdf/english/A{ac_no:03}/A{ac_no:03}P{part_no:03}.pdf'

    # if state_no == 'S16': ## Mizoram ## Not possible

    # if state_no == 'S17': ## Nagaland ## Not possible

    if state_no == 'S18': ## Odisha
        return f'http://ceoorissa.nic.in/ErollPdfs/{ac_no}/MotherRoll/Odiya/1/S18A{ac_no}P{part_no}.PDF'

    if state_no == 'S19': ## Punjab
        return f'https://www.ceopunjab.gov.in/erollpdf2/A{ac_no:03}/S21A{ac_no:03}P{part_no:03}.pdf'

    # if state_no == 'S20': ## Rajasthan ## Not possible

    if state_no == 'S21': ## Sikkim
        return f'https://ceosikkim.nic.in/UploadedFiles/ElectoralRollPolling/S21A{ac_no}P{part_no}.pdf'

    if state_no == 'S22':
        return f'https://www.elections.tn.gov.in/SSR2022_MR_05012022/dt{dist_no}/ac{ac_no:03}/ac{ac_no:03}{part_no:03}.pdf'



def get_language(state_no):

    # if state_no == 'S11': ## Andhra Pradesh
    #     return ('eng', 'english')

    # if state_no == 'S02': ## Arunachal Pradesh
    # #     return ('eng', 'english')

    # if state_no == 'S03': ## Assam
    #     return ('ass', 'assamese')

    # if state_no == 'S04': ## Bihar ## Not possible

    if state_no == 'S26': ## Chhattisgarh
        return ('hin', 'hindi')

    if state_no == 'S06': ## Gujarat
        return ('guj', 'gujarati')

    if state_no == 'S07': ## Haryana
        return ('hin', 'hindi')

    # if state_no == 'S08': ## Himachal Pradesh ## Not possible

    if state_no == 'S10': ## Karnataka
        return ('kan', 'kannada')

    # if state_no == 'S11': ## Kerala ## Not possible

    # if state_no == 'S12': ## Madhya Pradesh ## Not possible

    # if state_no == 'S13': ## Maharashtra ## Not possible

    if state_no == 'S14': ## Manipur
        return ('eng', 'english')

    if state_no == 'S15': ## Meghalaya
        return ('eng', 'english')

    # if state_no == 'S16': ## Mizoram ## Not possible

    # if state_no == 'S17': ## Nagaland ## Not possible

    if state_no == 'S18': ## Odisha
        return ('ori', 'oriya')

    if state_no == 'S19': ## Punjab
        return ('pan', 'punjabi')

    # if state_no == 'S20': ## Rajasthan ## Not possible

    if state_no == 'S21': ## Sikkim
        return ('eng', 'english')

    if state_no == 'S22':
        return ('tam', 'tamil')


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
    
    if district == 'null':
        district = ''
    if ac == 'null':
        ac = ''
    location = f'{state},{district},{ac}'
    r = None
    for i in range(5):
        (captcha_text, cookies) = await solve_captcha()

        print(captcha_text, cookies)
        r = requests.post('https://electoralsearch.in/Home/searchVoter', data={
            'age': dob,
            'gender': gender,  # M/F/O
            'location': location,
            'location_range': 20,
            'name': name,
            'page_no': '1',
            'results_per_page': '10',
            'reureureired': 'ca3ac2c8-4676-48eb-9129-4cdce3adf6ea',
            'rln_name': relative_name,
            'search_type': 'details',
            'txtCaptcha': captcha_text
        }, cookies=cookies)
        if r.text == 'Wrong Captcha':
            print('Wrong Captcha')
            continue
        else:
            break
    try:
        results = r.json()['response']['docs']
    except Exception as e:
        print(e)
        print(r.text)
        return {'error': 'Invalid captcha'}
    target = None
    if len(results) == 1:
        target = results[0]
        state = target['st_code']
        district = target['dist_no']
        ac = target['ac_no']
        part_no = target['part_no']
        if os.path.exists(f'dumps/{state}_{district}_{ac}_{part_no}.json'):
            with open(f'dumps/{state}_{district}_{ac}_{part_no}.json', 'r') as f:
                return get_family_tree(target,json.load(f))
        
        url = get_url(target['st_code'], int(target['dist_no']),
                      int(target['ac_no']), int(target['part_no']))
        dicts = []

        pdf = requests.get(url, verify=False).content
        pages = convert_from_bytes(pdf, 500)
        with Pool(cpu_count()//2) as p:
            texts = p.starmap(chop_image,[(pages[i], i + 1, get_language(state)[0]) for i in range(2, len(pages) - 1)])
        for tuples in texts:
            for text in tuples:
                dicts.append(parse_text(text[3], get_language(state)[1]))

        with open(f'dumps/{target["st_code"]}_{int(target["dist_no"])}_{int(target["ac_no"])}_{int(target["part_no"])}.json', 'w') as f:
            json.dump(dicts, f)

        return get_family_tree(target, dicts)

    elif len(results) == 0:
        return {'error': 'No results'}
    else:
        return {'error': 'Multiple results'}

@app.post('/trees')
async def get_tree(state,  district, ac, part_no):
    try:
        if os.path.exists(f'dumps/{state}_{district}_{ac}_{part_no}.json'):
            with open(f'dumps/{state}_{district}_{ac}_{part_no}.json', 'r') as f:
                return get_family_trees(json.load(f))
        
        url = get_url(state, int(district), int(ac), int(part_no))
                        
        dicts = []

        pdf = requests.get(url, verify=False).content
        pages = convert_from_bytes(pdf, 500)
        with Pool(cpu_count()//2) as p:
            texts = p.starmap(chop_image,[(pages[i], i + 1, get_language(state)[0]) for i in range(2, len(pages) - 1)])

        # Array of arrays of tuples to array of tuples
        texts = [text for texts in texts for text in texts]
        
        with Pool(cpu_count()//2) as p:
            dicts = p.starmap(parse_text,[(text[3], get_language(state)[1]) for text in texts])

        with open(f'dumps/{state}_{district}_{ac}_{part_no}.json', 'w') as f:
            json.dump(dicts, f)

        return get_family_trees(dicts)
    
    except Exception as e:
        print(e)
        return {'error': 'Invalid'}
