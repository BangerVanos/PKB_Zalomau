from app.backend.ontology_loader import OntologyLoader
import owlready2 as owl


class LoadProjects:

    @classmethod
    def load_projects(cls, onto: owl.Ontology | None):
        if onto is None:
            onto = OntologyLoader.load_ontology()
        return onto.Project.instances()
