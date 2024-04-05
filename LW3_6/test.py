from app.backend.ontology_loader import OntologyLoader


onto = OntologyLoader.load_ontology()
print(onto.Battle_Mechanics)
