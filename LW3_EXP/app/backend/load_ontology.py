import owlready2 as owl
import os


class LoadOntology:

    @classmethod
    def load(cls) -> owl.Ontology:
        try:            
            onto = owl.get_ontology(f'file://{os.path.realpath(os.path.join(
                os.path.dirname(__file__), '../ontology/game.owx'
            ))}').load()
        except Exception as err:
            raise err
        else:
            return onto
