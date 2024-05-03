from app.glue.player import Player
import owlready2 as owl
from app.backend.load_ontology import LoadOntology
from app.backend.fetch_from_onto import Fetcher, JSONFetcher
from enum import StrEnum
from random import choices, choice, randint
from typing import Literal


class GameState(StrEnum):
    idle = 'idle'
    figting = 'fighting'
    item = 'item'
    dead = 'dead'

    @classmethod
    def all(cls) -> list:
        '''All of the states except dead state'''
        return [
            cls.idle,
            cls.figting,
            cls.item            
        ]


class EventHandler:

    def __init__(self, player: Player, onto: owl.Ontology | None = None,
                 fetcher: Fetcher | None = None) -> None:
        self._player = player
        if onto is None:
            self._onto = LoadOntology.load()
        else:
            self._onto = onto
        if fetcher is None:
            self._fetcher = Fetcher(self._onto)
        else:
            self._fetcher = fetcher
        self._json = JSONFetcher(self._fetcher)
        self._state = GameState.idle
        self._current_enemy: dict | None = None
    
    def _select_state(self):
        self._state = choices(GameState.all(), (0.6, 0.2, 0.2))[0]
    
    def _create_enemy(self):
        lvl = max(1, randint(self._player.lvl - 1, self._player.lvl + 1))
        ap = randint(int(0.9 * self._player.max_ap),
                     int(1.1 * self._player.max_ap))
        max_ap = ap
        hp = randint(int(0.9 * self._player.max_hp),
                     int(1.1 * self._player.max_hp))
        max_hp = hp
        equipped_weapon = choice(self._onto.Firearm.instances())
        equipped_armor = choice(self._onto.Armor.instances())
        return {
            'lvl': lvl,
            'ap': ap,
            'hp': hp,
            'max_ap': max_ap,
            'max_hp': max_hp,
            'equipped_weapon': self._json.fetch_by_instance(equipped_weapon),
            'equipped_armor': self._json.fetch_by_instance(equipped_armor)
        }
    
    def step(self) -> str | None:
        self._player.restore_ap()
        self._select_state()
        event = self._handle_state()
        return event
    
    def _handle_state(self) -> str | None:
        if self._state == GameState.idle:
            return 'Nothing has happened! Continue walking...'
        elif self._state == GameState.item:
            item_name = self._random_item()
            return f'Congratulations! You\'ve found {item_name}!'
        elif self._state == GameState.figting:
            enemy = self._create_enemy()
            self._current_enemy = enemy
            return 'Enemy!'
    
    def enemy_interaction(self, _type: Literal['flee', 'attack', 'skip']) -> str | None:
        self._player.restore_ap()
        if _type == 'flee':
            event = self._try_to_flee()
        elif _type == 'attack':
            event = self._try_to_attack()
        elif _type == 'skip':
            event = 'Skipping move...'        
        if self._current_enemy is not None:
            event += '\n' + self._enemy_attack()
        return event

    def _try_to_flee(self) -> str | None:
        can_flee = choices((True, False), (0.3, 0.7))[0]
        if can_flee:
            event = 'Your flee attempt was successful!\n'
            self._state = GameState.idle
            self._current_enemy = None
        else:
            event = 'Your flee attempt was unsuccessfull\n'            
        return event
    
    def _try_to_attack(self) -> str | None:
        # Check for possibility of attack in context of AP
        ap_cost = self._player.weapon['ap_cost'][0]                       
        if not self._player.use_ap(ap_cost):
            event = 'Not enough AP!'
            return event 
        
        # If AP are enough
        weapon_accuracy = self._player.weapon['weapon_accuracy'][0]
        weapon_damage = self._player.weapon['weapon_damage'][0]
        missed = choices((False, True), (weapon_accuracy, 100 - weapon_accuracy))[0]
        if missed:
            event = 'You\'ve missed!'
        else:
            enemy_armor_pr = self._current_enemy['equipped_armor']['armor_protection'][0]
            old_hp = self._current_enemy['hp']
            self._current_enemy['hp'] = (
                self._current_enemy['hp'] - int(weapon_damage * (1 - enemy_armor_pr / 100))
            )
            event = f'You\'ve dealt {old_hp - self._current_enemy['hp']} damage to enemy!'
            if self._current_enemy['hp'] <= 0:
                self._player.add_xp(self._current_enemy['lvl'] * 100)
                event += '\n' + self._kill_enemy()                
                return event
        return event

    def _enemy_attack(self) -> None | str:

        # Enemy can restore some of its HP with 15% possibility
        restored_hp = choices((False, True), (0.85, 0.15))[0]
        if restored_hp:
            self._current_enemy['hp'] = min(self._current_enemy['max_hp'],
                                            int(self._current_enemy['hp'] * randint(110, 125) / 100))
            
        # Attack handling
        event = 'Enemy tried to attack you...'
        self._current_enemy['ap'] = min(self._current_enemy['max_ap'],
                                        int(self._current_enemy['ap'] * 1.1))
        
        # Handling AP demands
        ap_cost = self._current_enemy['equipped_weapon']['ap_cost'][0]
        if self._current_enemy['ap'] < ap_cost:
            event += '\n' + '...but its AP weren\'t enough!'
            return event
        
        # If AP are enough
        weapon_accuracy = self._current_enemy['equipped_weapon']['weapon_accuracy'][0]
        weapon_damage = self._current_enemy['equipped_weapon']['weapon_damage'][0]
        missed = choices((False, True), (weapon_accuracy, 100 - weapon_accuracy))[0]
        if missed:
            event += '\n' + '...but missed!'
        else:
            player_armor_pr = self._player.armor['armor_protection'][0]
            old_hp = self._player.hp
            self._player.take_damage(int(weapon_damage * (1 - player_armor_pr / 100)))
            event = f'...and dealt {old_hp - self._player.hp} damage to you!'
            if self._player.hp <= 0:
                event += '\n' + 'That attack killed you!'
                self._state = GameState.dead                
        return event
        

    def _kill_enemy(self) -> str | None:
        self._state = GameState.item
        self._current_enemy = None
        return 'Enemy is defeated! Trying to find something useful...'    
    
    def _random_item(self) -> str:
        item = choice(self._onto.Item.instances())
        self._player.add_item(item)
        return item.label[0]

    
    
    @property
    def enemy(self) -> None | dict:
        return self._current_enemy
    
    @property
    def state(self) -> str:
        return self._state
