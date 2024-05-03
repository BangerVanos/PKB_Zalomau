from app.glue.player import Player
import owlready2 as owl
from app.backend.load_ontology import LoadOntology


class EventHandler:

    def __init__(self, player: Player, onto: owl.Ontology | None = None) -> None:
        self._player = player
        if onto is None:
            self._onto = LoadOntology()
        else:
            self._onto = onto
