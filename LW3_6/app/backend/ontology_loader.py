import owlready2 as owl
import os


class OntologyLoader:

    @classmethod
    def load_ontology(cls) -> owl.Ontology:
        try:
            onto = owl.get_ontology(f'file://{os.path.realpath(os.path.join(
                os.path.dirname(__file__), '../ontology/game_studio_projects_ontology.owx'
            ))}').load()
        except Exception as err:
            raise err
        else:
            return onto
