from fuzzywuzzy import fuzz


def similar(a, b):
    return fuzz.ratio(a, b) > 80


def get_family_tree(target, people):
    relations = dict()
    relations['brother'] = []
    relations['sister'] = []
    relations['son'] = []
    relations['daughter'] = []
    relations['grandfather'] = []
    relations['grandmother'] = []
    relations['grandson'] = []
    relations['granddaughter'] = []
    for person in people:
        if similar(target['name'], person['name']) and target['age'] == person['age'] and similar(target['rln_name'], person['relation_name']):
            house_no = person['house_number']
            relationship_type = person['relationship_type']
            relation_name = person['relation_name']
            relations[relationship_type] = relation_name

    people = [person for person in people if person['house_number'] == house_no]
    relative = None
    son = None
    daughter = None
    for person in people:
        if similar(
                person['name'], relation_name):
            relations[relationship_type] = person['name']
            relative = person
    if relations.get('father') is not None:
        for person in people:
            if person['relationship_type'] == 'husband' and similar(
                    person['relation_name'], target['name']):
                relations['wife'] = person['name']
            if target['name'] != person['name'] and person['relationship_type'] == 'father' and similar(
                    person['relation_name'], relations['father']):
                if person['gender'] == 'male':
                    relations['brother'].append(person['name'])
                else:
                    relations['sister'].append(person['name'])
            if person['relationship_type'] == 'father' and similar(
                    person['relation_name'], target['name']):
                if person['gender'] == 'male':
                    relations['son'].append(person['name'])
                    son = person
                else:
                    relations['daughter'].append(person['name'])
                    daughter = person
            if relative is not None and (relationship_type == 'father' or relationship_type == 'mother') and relative['relationship_type'] == 'father' and similar(
                    relative['relation_name'], person['name']):
                relations['grandfather'].append(person['name'])
            if relative is not None and (relationship_type == 'father' or relationship_type == 'mother') and relative['relationship_type'] == 'mother' and similar(
                    relative['relation_name'], person['name']):
                relations['grandmother'].append(person['name'])
            if son and person['relationship_type'] == 'father' and similar(
                    person['relation_name'], son['name']):
                relations['grandson'].append(person['name'])
            if daughter is not None and person['relationship_type'] == 'father' and similar(
                    person['relation_name'], daughter['name']):
                relations['granddaughter'].append(person['name'])
    for person in people:
        if person['name'] not in relations.values():
            print(person['name'])
    return relations
