from typing import List
import csv
import logging
from indictrans import Transliterator
import re
csv_file_path = 'output.csv'


def translate_to_eng(string: str, language: str):
    if language == 'english':
        return string
    if language == 'tamil':
        return Transliterator(source='tam', target='eng', build_lookup=True).transform(string)
    if language == 'hindi':
        return Transliterator(source='hin', target='eng', build_lookup=True).transform(string)
    if language == 'punjabi':
        return Transliterator(source='pan', target='eng', build_lookup=True).transform(string)
    if language == 'kannada':
        return Transliterator(source='kan', target='eng', build_lookup=True).transform(string)
    if language == 'oriya':
        return Transliterator(source='ori', target='eng', build_lookup=True).transform(string)

def get_relationship_type(relation: str, language: str = 'english') -> str:
    if language == 'english':
        if 'father' in relation.lower():
            return 'father'
        elif 'mother' in relation.lower():
            return 'mother'
        elif 'wife' in relation.lower():
            return 'wife'
        elif 'husband' in relation.lower():
            return 'husband'
        else:
            return 'other'
    elif language == 'tamil':
        if 'தந்தை' in relation:
            return 'father'
        elif 'தாய்' in relation:
            return 'mother'
        elif 'கணவர்' in relation:
            return 'husband'
        elif 'மனைவி' in relation:
            return 'wife'
        else:
            return 'other'
    elif language == 'hindi':
        if 'पिता' in relation:
            return 'father'
        elif 'माता' in relation:
            return 'mother'
        elif 'पति' in relation:
            return 'husband'
        elif 'पत्नी' in relation:
            return 'wife'
        else:
            return 'other'
    elif language == 'punjabi':
        if 'ਪਿਤਾ' in relation:
            return 'father'
        elif 'ਮਾਤਾ' in relation:
            return 'mother'
        elif 'ਪਤੀ' in relation:
            return 'husband'
        elif 'ਪਤਨੀ' in relation:
            return 'wife'
        else:
            return 'other'
    elif language == 'kannada':
        if 'ತಂದೆ' in relation:
            return 'father'
        elif 'ತಾಯಿ' in relation:
            return 'mother'
        elif 'ಸ್ವತಂತ್ರರೂಪ' in relation:
            return 'husband'
        elif 'ಸ್ವತಂತ್ರರೂಪಿನ' in relation:
            return 'wife'
        else:
            return 'other'
    elif language == 'oriya':
        if 'ପିତା' in relation:
            return 'father'
        elif 'ମାତା' in relation:
            return 'mother'
        elif 'ପତି' in relation:
            return 'husband'
        elif 'ପତିନି' in relation:
            return 'wife'
        else:
            return 'other'
    return 'other'


def get_gender(gender: str, language: str = 'english') -> str:
    if language == 'english':
        return gender.lower()
    elif language == 'tamil':
        if 'ஆண்' in gender:
            return 'male'
        elif 'பெண்' in gender:
            return 'female'
        else:
            return 'other'
    elif language == 'hindi':
        if 'पुरुष' in gender:
            return 'male'
        elif 'महिला' in gender:
            return 'female'
        else:
            return 'other'
    elif language == 'punjabi':
        if 'ਪੁਰੁ਷' in gender:
            return 'male'
        elif 'ਸਤ੍ਰੀ' in gender:
            return 'female'
        else:
            return 'other'

    elif language == 'kannada':
        if 'ಪುರುಷ' in gender:
            return 'male'
        elif 'ಸ್ತ್ರೀ' in gender:
            return 'female'
        else:
            return 'other'

    elif language == 'oriya':
        if 'ପୁରୁଷ' in gender:
            return 'male'
        elif 'ସ୍ତ୍ରୀ' in gender:
            return 'female'
        else:
            return 'other'
    return 'other'


def extract_name(lines: List[str], language='english'):
    if not lines:
        return '---', []
    name = lines[0].split(':')
    slice_index = 1
    if len(name) != 2:
        name = '---'
    else:
        name = name[1].strip()

    # check if name continues to next line
    if len(lines) > 1 and ':' not in lines[1]:
        name = name + ' ' + lines[1].strip()
        slice_index = 2
    print(name)
    name = translate_to_eng(name, language)
    print(name)
    name = re.sub('[-]+', '', name).strip()
    return name, lines[slice_index:]


def extract_relationship(lines: List[str], language='english'):
    if not lines:
        return '---', '---', []
    relation_name = lines[0].split(':')
    slice_index = 1
    if len(relation_name) != 2:
        relation_name = '---'
        relation_type = get_relationship_type(relation_name[0], language)
    else:
        relation_type = get_relationship_type(relation_name[0], language)
        relation_name = relation_name[1].strip()

    # check if name continues to next line
    if len(lines) > 1 and ':' not in lines[1]:
        relation_name = relation_name + ' ' + lines[1].strip()
        slice_index = 2
    relation_name = translate_to_eng(relation_name, language)
    relation_name = re.sub('[-]+', '', relation_name).strip()
    return relation_name, relation_type, lines[slice_index:]


def extract_house_number(lines: List[str], language='english'):
    if not lines:
        return '---', []
    house_number = lines[0].split(':')
    slice_index = 1
    if len(house_number) != 2:
        house_number = '---'
    else:
        house_number = house_number[1].strip()
    house_number = translate_to_eng(house_number, language)
    return house_number, lines[slice_index:]


def extract_age_and_gender(lines: List[str], language='english'):
    if not lines:
        return '---', '---'
    age = lines[0].split(':')
    if len(age) != 3:
        age = '---'
    else:
        age = age[1].strip().split(' ')[0]

    gender = lines[0].split(':')
    if len(gender) != 3:
        gender = '---'
    else:
        gender = get_gender(gender[2].strip(), language)
    return age, gender


def parse_text(text, language='english') -> dict:
    # splitlines
    lines = text.splitlines()
    # remove empty lines
    lines = [line for line in lines if line]
    # remove lines with only whitespace
    lines = [line.strip() for line in lines if line.strip()]
    voter_details = dict()
    try:
        name_info = extract_name(lines, language)
        voter_details['name'] = name_info[0]
        remaining_data = name_info[1]
        relation_name, relationship_type, remaining_data = extract_relationship(
            remaining_data, language)
        voter_details['relation_name'] = relation_name
        voter_details['relationship_type'] = relationship_type

        voter_details['house_number'], remaining_data = extract_house_number(
            remaining_data, language)

        age, gender = extract_age_and_gender(remaining_data, language)
        voter_details['age'] = age
        voter_details['gender'] = gender
        return voter_details
    except Exception as e:
        # print traceback
        logging.exception(e)
        # return {}
        raise e


if __name__ == '__main__':
    with open('output.csv') as f:
        # read csv
        reader = csv.reader(f, delimiter=',')
        i = 0
        for row in reader:
            # if i == 1:
            #     break
            i += 1
            voter_details = parse_text(row[3], 'tamil')
            print(voter_details)
