import owlready2 as owl
from app.backend.fetch_from_onto import Fetcher, JSONFetcher
from enum import StrEnum


class Player:

    def __init__(self, character_uri: str,
                 fetcher: Fetcher | None = None) -> None:
        if fetcher is None:
            self._fetcher = Fetcher()            
        else:
            self._fetcher = fetcher
        self._json = JSONFetcher(self._fetcher)
        self._character = self._fetcher.fetch_by_uri(character_uri)

    def item_use(self, ind: int, uri: str):
        item = self._fetcher.fetch_by_uri(uri)
        if self._is_item_usable(item):
            self._apply_item(item, ind)

    def _is_item_usable(self, item) -> bool:
        if len(item.used_only_by) == 0:
            return True
        return self._character.character_class in item.used_only_by

    def _apply_item(self, item, ind) -> None:
        item_class = item.is_a[0].name
        if item_class == 'Firearm':
            self._apply_weapon(item)
        elif 'Armor' in item_class:
            self._apply_armor(item)
        elif item_class == 'HealingItem':
            self._apply_heal(item, ind)

    def _apply_weapon(self, weapon) -> None:
        self._character.equipped_weapon = weapon

    def _apply_armor(self, armor) -> None:
        self._character.equipped_armor = armor

    def _apply_heal(self, heal, ind: int) -> None:
        if self._character.hp == self.max_hp:
            return
        self._character.hp += round(
            self.max_hp * heal.restored_hp / 100
        )
        self._character.item_of_inv.pop(ind)

    def take_damage(self, damage: int) -> None:
        self._character.hp = min(0, self._character.hp - damage)

    def use_ap(self, ap_amount: int) -> bool:
        if self._character.ap < ap_amount:
            return False
        else:
            self._character.ap -= ap_amount
            return True

    def add_item(self, item) -> None:
        self._character.item_of_inv.append(item)              
    
    @property
    def character_json(self) -> dict:
        return self._json.fetch_by_instance(self._character)
    
    @property
    def hp(self) -> int:
        return self._character.hp
    
    @property
    def ap(self) -> int:
        return self._character.ap
    
    @property
    def lvl(self) -> int:
        return self._character.lvl
    
    @property
    def xp(self) -> int:
        return self._character.exp
    
    @property
    def weapon(self) -> dict:
        return self._json.fetch_by_instance(self._character.equipped_weapon)
    
    @property
    def armor(self) -> dict:
        return self._json.fetch_by_instance(self._character.equipped_armor)
    
    @property
    def inv(self) -> list[dict]:
        return [self._json.fetch_by_instance(item) for item
                in self._character.item_of_inv]
    
    @property
    def max_hp(self) -> int:
        base_hp = self._character.character_class.base_hp
        hp_coeff = self._character.character_class.hp_coeff
        return base_hp*(hp_coeff**(self._character.lvl - 1))
    
    @property
    def max_ap(self) -> int:
        base_ap = self._character.character_class.base_ap
        ap_coeff = self._character.character_class.ap_coeff
        return base_ap*(ap_coeff**(self._character.lvl - 1))
