# Import Json
import json

def create_family_tree():
    with open('family.json') as f:
        family_tree = json.load(f)

        family_dict = {}
        for member in family_tree:
            if family_dict.get(member['house_number']) is None:
                family_dict[member['house_number']] = [member]
            else:
                family_dict[member['house_number']].append(member)

        relations = dict()
        for key, same_family in family_dict.items():
            for member in same_family:
                if member['relation_name'] in [value['name'] for value in same_family]:
                    if relations.get(member['relation_name']) is not None:
                        relations[member['house_number']].append({
                            'name': member['name'],
                            'relation_name': member['relation_name'],
                            'relationship_type': member['relationship_type']
                        })
                    else:
                        relations[member['house_number']] = [{
                            'name': member['name'],
                            'relation_name': member['relation_name'],
                            'relationship_type': member['relationship_type']
                        }]


create_family_tree()

