import owlready2 as owl
from app.backend.fetch_from_onto import Fetcher, JSONFetcher
from enum import StrEnum
from math import log, floor


class Player:

    def __init__(self, character_uri: str,
                 fetcher: Fetcher | None = None) -> None:
        if fetcher is None:
            self._fetcher = Fetcher()            
        else:
            self._fetcher = fetcher
        self._json = JSONFetcher(self._fetcher)
        self._character = self._fetcher.fetch_by_uri(character_uri)

    def item_use(self, ind: int, uri: str) -> None | str:
        item = self._fetcher.fetch_by_uri(uri)
        if self._is_item_usable(item):
            event = self._apply_item(item, ind)
        else:
            event = f'Can\' use item: {item.label[0]}'
        return event

    def _is_item_usable(self, item) -> bool:
        if len(item.used_only_by) == 0:
            return True
        return self._character.character_class in item.used_only_by

    def _apply_item(self, item, ind) -> None | str:
        item_class = item.is_a[0].name
        if item_class == 'Firearm':
            event = self._apply_weapon(item)
        elif 'Armor' in item_class:
            event = self._apply_armor(item)
        elif item_class == 'HealingItem':
            event = self._apply_heal(item, ind)
        return event

    def _apply_weapon(self, weapon) -> None | str:
        self._character.equipped_weapon = weapon
        return f'Equipped {weapon.label[0]}'

    def _apply_armor(self, armor) -> None | str:
        self._character.equipped_armor = armor
        return f'Equipped {armor.label[0]}'

    def _apply_heal(self, heal, ind: int) -> None | str:
        if self._character.hp == self.max_hp:
            return 'Your HP is full!'
        old_hp = self._character.hp
        self._character.hp += round(
            self.max_hp * heal.restored_hp / 100
        )
        self._character.hp = min(self.max_hp, self._character.hp)
        self._character.item_of_inv.pop(ind)
        return f'Successfully restored {self._character.hp - old_hp} HP!'

    def take_damage(self, damage: int) -> None:
        self._character.hp = int(
            max(0, self._character.hp - damage)
        )

    def use_ap(self, ap_amount: int) -> bool:                      
        if self._character.ap < ap_amount:
            return False
        else:
            self._character.ap -= ap_amount
            return True

    def add_item(self, item) -> None:
        self._character.item_of_inv.append(item)

    def add_xp(self, xp: int) -> None:
        self._character.exp += xp
        self._count_lvl()    

    def _count_lvl(self) -> None:
        lvl_q = 1.5
        base_xp = 100
        old_lvl = self._character.lvl
        self._character.lvl = floor(log(self._character.exp * (lvl_q - 1) / 
                                    base_xp + 1, lvl_q))
        if self._character.lvl > old_lvl:
            self._character.hp = self.max_hp
            self._character.ap = self.max_ap

    def restore_ap(self) -> None:
        self._character.ap = int(
            min(self.max_ap, self._character.ap + int(0.25 * self.max_ap))
        )

    def die(self) -> None:
        '''If you die, you just roll back to start stats'''
        self._character.xp = 0
        self._character.lvl = 1
        self._character.exp = 0

        # Class-based-stats
        character_class = self._character.character_class
        self._character.equipped_weapon = character_class.start_weapon
        self._character.equipped_armor = character_class.start_armor

        self._character.ap = character_class.base_ap
        self._character.hp = character_class.base_hp

        hp_kit = self._fetcher.fetch_by_uri('hp_kit_small')
        self._character.item_of_inv = [character_class.start_weapon,
                                       character_class.start_armor,
                                       hp_kit]          
    
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
        return int(base_hp*(hp_coeff**(self._character.lvl - 1)))
    
    @property
    def max_ap(self) -> int:
        base_ap = self._character.character_class.base_ap
        ap_coeff = self._character.character_class.ap_coeff
        return int(base_ap*(ap_coeff**(self._character.lvl - 1)))
