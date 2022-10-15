from typing import List, Dict
import csv
import logging

csv_file_path = 'output.csv'


def get_relationship_type(relation: str, language: str = 'english') -> str:
    if language == 'english':
        return relation.lower()
    elif language == 'tamil':
        if 'தந்தை' in relation:
            return 'father'
        elif 'தாய்' in relation:
            return 'mother'
        # kanavar
        elif 'கணவர்' in relation:
            return 'husband'
        # manaivi
        elif 'மனைவி' in relation:
            return 'wife'
        else:
            return 'other'
    return 'other'


def get_gender(gender: str, language: str = 'english') -> str:
    if language == 'english':
        return gender.upper()[0]
    elif language == 'tamil':
        if 'ஆண்' in gender:
            return 'M'
        elif 'பெண்' in gender:
            return 'F'
        else:
            return 'O'
    return 'O'


def extract_name(lines: List[str]):
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
    return relation_name, relation_type, lines[slice_index:]


def extract_house_number(lines: List[str]):
    if not lines:
        return '---', []
    house_number = lines[0].split(':')
    slice_index = 1
    if len(house_number) != 2:
        house_number = '---'
    else:
        house_number = house_number[1].strip()

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
        name_info = extract_name(lines)
        voter_details['name'] = name_info[0]
        remaining_data = name_info[1]
        relation_name, relationship_type, remaining_data = extract_relationship(
            remaining_data, language)
        voter_details['relation_name'] = relation_name
        voter_details['relationship_type'] = relationship_type

        voter_details['house_number'], remaining_data = extract_house_number(
            remaining_data)

        age, gender = extract_age_and_gender(remaining_data, language)
        voter_details['age'] = age
        voter_details['gender'] = gender
        return voter_details
    except Exception as e:
        # print traceback
        logging.exception(e)
        # return {}
        raise e
