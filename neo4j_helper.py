from neo4j import GraphDatabase

class Database:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def define_relationship(self, relationship_object):
        with self.driver.session() as session:
            session.execute_write(self._define_relationship, relationship_object)
        

    @staticmethod
    def _define_relationship(tx, relationship_object):
        # Create a relationship between two nodes
        person1 = relationship_object['person1']
        person2 = relationship_object['person2']
        relationship_type = relationship_object['relationship_type']
        house_number = relationship_object['house_number']
        
        # Create a relationship between two nodes

        # Create persons if they don't exist and  create a relationship between them
        tx.run("MERGE (a:Person {name: $person1, house_number: $house_number}) "
                "MERGE (b:Person {name: $person2, house_number: $house_number}) "
                "MERGE (a)-[r:" + relationship_type + "]->(b)", person1=person1, person2=person2, house_number=house_number)


# if __name__ == "__main__":
#     connection = Database("bolt://localhost:7687", "neo4j", "password")
#     connection.define_relationship(
#         {
#             'person1':  'John',
#             'person2': 'Jane',
#             'relationship_type': 'HUSBAND',
#             'house_number': 1
#         }
#     )