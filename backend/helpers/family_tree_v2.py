from dataclasses import dataclass
import json
from fuzzywuzzy import fuzz

from helpers.neo4j_helper import connection

def similar(a, b):
    return fuzz.WRatio(a, b) > 90

def similarity(a, b):
    return fuzz.WRatio(a, b)


@dataclass
class Node:
    id: str
    name: str
    age: str
    gender: str
    house_number: str
    ancestor: "Node"
    ancestor_type: str
    spouse: "Node"
    spouse_name: str
    children: list[("Node", str)]

@dataclass
class Person:
    name: str
    relationship_type: str
    relation_name: str
    house_number: str
    age: str
    gender: str


def build_graph(people: list[Person]) -> dict[str, Node]:
    nodes: dict[str, Node] = {}
    for person in people:
        id = f'{person.name}-{person.house_number}'
        nodes[id] = Node(id, person.name, person.age, person.gender, person.house_number, None, None, None, None, [])
        relation = f'{person.relation_name}-{person.house_number}'
        if relation not in nodes:
            nodes[relation] = Node(relation, person.relation_name, None, None, person.house_number, None, None, None, None, [])


    # Node in same house
    node_in_same_house = {}
    for node in nodes:
        if nodes[node].house_number not in node_in_same_house:
            node_in_same_house[nodes[node].house_number] = []
        node_in_same_house[nodes[node].house_number].append(nodes[node])

    
    for person in people:
        id = f'{person.name}-{person.house_number}'
        max_similarity = 0
        max_node = None
        for node in nodes:
            if nodes[node].house_number == person.house_number:
                if similarity(nodes[node].name, person.relation_name) > max_similarity:
                    max_similarity = similarity(nodes[node].name, person.relation_name)
                    max_node = node
                    # GET PERSON WITH HIGHEST SIMILARITY
        if max_node and max_similarity > 83:
            node = max_node
            if person.relationship_type in ['father', 'mother']:
                nodes[id].ancestor = nodes[node]
                nodes[id].ancestor_type = person.relationship_type
                nodes[node].children.append((nodes[id], person.relation_name))
            elif person.relationship_type in ['husband', 'wife']:
                nodes[node].spouse = nodes[id]
                nodes[id].spouse = nodes[node]
                nodes[id].spouse_name = person.relation_name
    return nodes

def dump_visualization():
    with open('data.json', 'r') as f:
        people = json.load(f)
        people = [Person(**person) for person in people]
        nodes = build_graph(people)
        ds_nodes = [{'id': node.id, 'label': f'{node.name}\nHouse no.: {node.house_number}', 'house_number': node.house_number } for node in nodes.values() if node.ancestor or node.spouse or node.children]
        ds_edges = []
        for node in nodes:
            if nodes[node].spouse and nodes[node].gender == 'male':
                name = nodes[node].spouse_name or nodes[node].spouse.spouse_name or 'None'
                ds_edges.append({'from': nodes[node].id, 'to': nodes[node].spouse.id, 'label': f'spouse ({name})'})
            for child, name in nodes[node].children:
                ds_edges.append({'from': nodes[node].id, 'to': child.id, 'label': f'child ({name})', 'arrows': 'to'})
        json.dump({'nodes': ds_nodes, 'edges': ds_edges}, open('family_tree.json', 'w'))

def get_family_tree(target, people: list[Person]) -> Node:
    
    people = [Person(person['name'], person['relationship_type'], person['relation_name'], person['house_number'], person['age'], person['gender']) for person in people]
    house_no = None
    print(target)
    for person in people:
        if similar(target['name'], person.name) :
            print(person.name, person.age)
            house_no = person.house_number
    nodes = build_graph(people)
    ds_nodes = [{'id': node.id, 'label': f'{node.name}\nHouse no.: {node.house_number}', 'house_number': node.house_number } for node in nodes.values() if node.house_number == house_no]
    ds_edges = []
    for node in nodes:
        if nodes[node].spouse and nodes[node].gender == 'male':
            name = nodes[node].spouse_name or nodes[node].spouse.spouse_name or 'None'
            ds_edges.append({'from': nodes[node].id, 'to': nodes[node].spouse.id, 'label': f'spouse ({name})'})
            ds_edges.append({'from': nodes[node].spouse.id, 'to': nodes[node].id, 'label': f'spouse ({name})'})
        for child, name in nodes[node].children:
            ds_edges.append({'from': nodes[node].id, 'to': child.id, 'label': f'child ({name})', 'arrows': 'to'})
    return {'nodes': ds_nodes, 'edges': ds_edges}

def get_family_tree_json(target, people: list[Person]) -> str:
    return json.dumps(get_family_tree(target, people), default=lambda o: o.__dict__)

def get_family_trees(people: list[Person]) -> list[Node]:
    people = [Person(person['name'], person['relationship_type'], person['relation_name'], person['house_number'], person['age'], person['gender']) for person in people]
    nodes = build_graph(people)
    ds_nodes = [{'id': node.id, 'label': f'{node.name}\nHouse no.: {node.house_number}', 'house_number': node.house_number } for node in nodes.values() if node.ancestor or node.spouse or node.children]
    ds_edges = []
    for node in nodes:
        if nodes[node].spouse and nodes[node].gender == 'male':
            name = nodes[node].spouse_name or nodes[node].spouse.spouse_name or 'None'
            ds_edges.append({'from': nodes[node].id, 'to': nodes[node].spouse.id, 'label': f'spouse ({name})'})
            ds_edges.append({'from': nodes[node].spouse.id, 'to': nodes[node].id, 'label': f'spouse ({name})'})
            # connection.define_relationship({
            #     'person1': nodes[node].name,
            #     'person2': nodes[node].spouse.name,
            #     'relationship_type': 'spouse',
            #     'house_number': nodes[node].house_number
            # })
            # connection.define_relationship({
            #     'person1': nodes[node].spouse.name,
            #     'person2': nodes[node].name,
            #     'relationship_type': 'spouse',
            #     'house_number': nodes[node].house_number
            # })

        for child, name in nodes[node].children:
            ds_edges.append({'from': nodes[node].id, 'to': child.id, 'label': f'child ({name})', 'arrows': 'to'})
            # connection.define_relationship({
            #     'person1': nodes[node].name,
            #     'person2': child.name,
            #     'relationship_type': 'child',
            #     'house_number': nodes[node].house_number
            # })
    return {'nodes': ds_nodes, 'edges': ds_edges}
