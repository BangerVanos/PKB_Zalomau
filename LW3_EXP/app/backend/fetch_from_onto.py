import owlready2 as owl
from app.backend.load_ontology import LoadOntology
from typing import Iterable


class Fetcher:

    def __init__(self, onto: owl.Ontology | None = None) -> None:
        if onto is None:
            self._onto = LoadOntology.load()
        else:
            self._onto = onto
    
    def fetch_all_onto_classes(self) -> tuple[owl.ThingClass]:
        return tuple(self._onto.classes())
    
    def fetch_all_character_classes(self) -> tuple:
        return tuple(self._onto.CharacterClass.instances())
    
    def fetch_all_characters(self) -> tuple:
        return tuple(self._onto.Character.instances())
    
    def fetch_character_class_id(self, _id: int = 0):
        return self.fetch_all_character_classes()[_id]
    
    def fetch_by_uri(self, uri: str):
        uri = uri.split('.')[-1]
        return self._onto[uri]


class JSONFetcher:

    def __init__(self, fetcher: Fetcher | None = None) -> None:
        if fetcher is None:
            self._fetcher = Fetcher()
        else:
            self._fetcher = fetcher
    
    def fetch_by_instance(self, instance) -> dict:
        props = {prop.name: (prop[instance][0] if isinstance(prop, owl.FunctionalProperty)
                 else prop[instance]) for prop in instance.get_properties()}
        props['uri'] = str(instance)
        return props
    
    def fetch_by_uri(self, uri: str):
        inst = self._fetcher.fetch_by_uri(uri)
        props = self.fetch_by_instance(inst)
        props['uri'] = uri          
        return props

    def fetch_instances(self, instances: Iterable) -> list[dict]:
        return [self.fetch_by_instance(inst)
                for inst in instances]
    
    def fetch_all_character_classes(self) -> list[dict]:
        raw = self._fetcher.fetch_all_character_classes()        
        return self.fetch_instances(raw)
    
    def fetch_all_characters(self) -> list[dict]:
        raw = self._fetcher.fetch_all_characters()
        return self.fetch_instances(raw)
