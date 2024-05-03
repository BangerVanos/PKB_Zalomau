import streamlit as st
from app.backend.fetch_from_onto import JSONFetcher
from app.glue.player import Player
from app.glue.event_handler import EventHandler
from streamlit_extras.card import card
from streamlit_extras.row import row
from typing import Literal


class MainGameView:

    def __init__(self) -> None:
        self._character_uri = st.session_state.get('selected_character', None)
        self._fetcher = JSONFetcher()

    def run(self) -> None:
        if self._character_uri is None:
            st.error('## You must select character first!')
        else:
            if st.session_state.get('player') is None:
                st.session_state['player'] = Player(self._character_uri)
                st.session_state['event_handler'] = EventHandler(st.session_state['player'])
            self._load_main_game(self._character_uri)
            
    
    def _load_main_game(self, uri: str) -> None:
        player: Player = st.session_state.get('player')
        event_handler: EventHandler = st.session_state.get('event_handler')        

        stat_cols = st.columns([1, 1, 2])

        # Fetching player stats
        armor = player.armor
        weapon = player.weapon

        armor_img = armor['image'][0]
        weapon_img = weapon['image'][0]
        armor_label = f'{armor['label'][0]} (PR {armor['armor_protection'][0]}%)'
        weapon_label = f'{weapon['label'][0]} (DMG {weapon['weapon_damage'][0]} AP {weapon['ap_cost'][0]})' 

        with stat_cols[0]:
            st.write('### My stats')
            st.image(image=[armor_img, weapon_img],
                     caption=[armor_label, weapon_label],
                     use_column_width=True)
            stat_row = row(4)
            stat_row.metric(label='HP', value=player.hp)
            stat_row.metric(label='AP', value=player.ap)
            stat_row.metric(label='LVL', value=player.lvl)
            stat_row.metric(label='XP', value=player.xp)

            # Render event buttons            
            self._render_event_items(event_handler)

        with stat_cols[1]:
            st.write('### Enemy stats')
            self._render_enemy(event_handler)
        with stat_cols[2]:
            st.write('### Events')
            self._event_placeholder = st.container(border=True)
        st.write('## My Inventory')
        self._render_inventory(player)
    
    def _new_event(self, placeholder, event: str):
        with placeholder:
            events = event.split('\n')
            for event in events:
                st.write(event)
            st.divider()
    
    def _render_inventory(self, player: Player) -> None:
        inv = player.inv
        inv_container = st.container(border=True, height=300)                
        for ind, item in enumerate(inv):            
            with inv_container:
                card(
                    title=item['label'][0],
                    image=item['image'][0],
                    text=item['label'][0],
                    on_click=(lambda ind=ind, uri=item['uri'],
                              item=item: self._handle_item_click(ind, uri, item,
                                                                 player)),
                    key=f'item_{ind}'
                )            
    
    def _handle_item_click(self, ind: int, uri: str, item: dict,
                           player: Player) -> None:
        event = player.item_use(ind, uri)
        self._new_event(self._event_placeholder,
                        f'Tried to use: {item['label'][0]} \n {event}')                        

    def _render_event_items(self, event_handler: EventHandler) -> None:        
        if event_handler.state == 'fighting':
            cols = st.columns([1, 1, 2])
            with cols[0]:
                st.button('Flee', use_container_width=True,
                          key='fight_flee',
                          on_click=lambda: self._enemy_interaction(event_handler, 'flee'))
            with cols[1]:
                st.button('Skip', use_container_width=True,
                          key='fight_skip',
                          on_click=lambda: self._enemy_interaction(event_handler, 'skip'))
            with cols[2]:
                st.button('Attack', use_container_width=True,
                          key='fight_attack',
                          on_click=lambda: self._enemy_interaction(event_handler, 'attack'))           
        else:
            st.button(label='Go ->', key='go_btn',
                      help='Next step of your life',
                      on_click=lambda: self._step(event_handler),
                      use_container_width=True)

    def _step(self, event_handler: EventHandler) -> None:
        st.session_state.get('player').restore_ap()
        event = event_handler.step()
        self._new_event(self._event_placeholder, event)    
    
    def _enemy_interaction(self, event_handler: EventHandler,
                           _type: Literal['flee', 'attack', 'skip']) -> None:
        event = event_handler.enemy_interaction(_type)
        self._new_event(self._event_placeholder, event)
        
    def _render_enemy(self, event_handler: EventHandler) -> None:
        if (enemy := event_handler.enemy) is None:
            return
        armor = enemy['equipped_armor']
        weapon = enemy['equipped_weapon']

        armor_img = armor['image'][0]
        weapon_img = weapon['image'][0]
        armor_label = f'{armor['label'][0]} (PR {armor['armor_protection'][0]}%)'
        weapon_label = f'{weapon['label'][0]} (DMG {weapon['weapon_damage'][0]} AP {weapon['ap_cost'][0]})'

        st.image(image=[armor_img, weapon_img],
                     caption=[armor_label, weapon_label],
                     use_column_width=True)
        stat_row = row(3)                    
        stat_row.metric(label='LVL', value=enemy['lvl'])
        stat_row.metric(label='HP', value=enemy['hp'])
        stat_row.metric(label='AP', value=enemy['ap'])


view = MainGameView()
view.run()
