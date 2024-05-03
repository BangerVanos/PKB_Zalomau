import owlready2 as owl
from app.backend.load_ontology import LoadOntology
from app.backend.load_ontology import SaveOntology
from app.backend.fetch_from_onto import Fetcher


class IndividualCreator:

    def __init__(self, onto: owl.Ontology | None = None,
                 fetcher: Fetcher | None = None) -> None:
        if onto is None:
            self._onto = LoadOntology.load()
        if fetcher is None:
            self._fetcher = Fetcher(onto)
    
    def create_new_character(self, class_uri: str):
        new_character = self._onto.Character()
        character_class = self._fetcher.fetch_by_uri(class_uri)

        # Defining object properties
        new_character.character_class = character_class
        new_character.equipped_weapon = character_class.start_weapon
        new_character.equipped_armor = character_class.start_armor
        new_character.item_of_inv = [character_class.start_weapon,
                                     character_class.start_armor,
                                     self._onto.hp_kit_small]
        
        # Defining data properties
        new_character.lvl = 1
        new_character.ap = character_class.base_ap
        new_character.hp = character_class.base_hp
        new_character.exp = 0

        # Saving to ontology
        SaveOntology.save(self._onto)        

        return new_character
    
    def destroy_individual(self, uri: str) -> None:
        individual = self._fetcher.fetch_by_uri(uri)
        owl.destroy_entity(individual)

        return individual
