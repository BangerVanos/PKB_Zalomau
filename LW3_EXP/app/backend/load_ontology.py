import owlready2 as owl
import os


class LoadOntology:

    @classmethod
    def load(cls) -> owl.Ontology:
        try:            
            onto = owl.get_ontology(f'file://{os.path.realpath(os.path.join(
                os.path.dirname(__file__), '../ontology/game.rdf'
            ))}').load()
        except Exception as err:
            raise err
        else:
            return onto


class SaveOntology:

    @classmethod
    def save(cls, onto: owl.Ontology) -> None:
        try:
            onto.save(file=os.path.realpath(
                os.path.join(
                    os.path.dirname(__file__), '../ontology/game.rdf'
                )
            ), format='rdfxml')
        except Exception as err:
            print(err)
            raise err
        
