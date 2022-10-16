from dataclasses import dataclass
import json
from fuzzywuzzy import fuzz


def similar(a, b):
    return fuzz.WRatio(a, b) > 90


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
        id = f'{person.name}-{person.house_number}-{person.age}'
        nodes[id] = Node(id, person.name, person.age, person.gender, person.house_number, None, None, None, None, [])
    for person in people:
        id = f'{person.name}-{person.house_number}-{person.age}'
        for node in nodes:
            if nodes[node].house_number == person.house_number:
                if similar(nodes[node].name, person.relation_name):
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
        ds_nodes = [{'id': node.id, 'label': f'{node.name}\nHouse no.: {node.house_number}'} for node in nodes.values() if node.ancestor or node.spouse or node.children]
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
    graph = build_graph(people)
    return graph[f'{target["name"]}-{target["house_number"]}-{target["age"]}']

def get_family_tree_json(target, people: list[Person]) -> str:
    return json.dumps(get_family_tree(target, people), default=lambda o: o.__dict__)

def get_family_trees(people: list[Person]) -> list[Node]:
    people = [Person(person['name'], person['relationship_type'], person['relation_name'], person['house_number'], person['age'], person['gender']) for person in people]
    nodes = build_graph(people)
    ds_nodes = [{'id': node.id, 'label': f'{node.name}\nHouse no.: {node.house_number}'} for node in nodes.values() if node.ancestor or node.spouse or node.children]
    ds_edges = []
    for node in nodes:
        if nodes[node].spouse and nodes[node].gender == 'male':
            name = nodes[node].spouse_name or nodes[node].spouse.spouse_name or 'None'
            ds_edges.append({'from': nodes[node].id, 'to': nodes[node].spouse.id, 'label': f'spouse ({name})'})
        for child, name in nodes[node].children:
            ds_edges.append({'from': nodes[node].id, 'to': child.id, 'label': f'child ({name})', 'arrows': 'to'})
    return {'nodes': ds_nodes, 'edges': ds_edges}