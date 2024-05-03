import streamlit as st
from app.backend.fetch_from_onto import JSONFetcher
from app.glue.player import Player
from streamlit_extras.card import card
from streamlit_extras.row import row


class MainGameView:

    def __init__(self) -> None:
        self._character_uri = st.session_state.get('selected_character', None)
        self._fetcher = JSONFetcher()

    def run(self) -> None:
        if self._character_uri is None:
            st.error('## You must select character first!')
        else:
            self._load_main_game(self._character_uri)
            
    
    def _load_main_game(self, uri: str) -> None:
        player = Player(uri)        

        stat_cols = st.columns([1, 1, 2])

        # Fetching player stats
        armor = player.armor
        weapon = player.weapon

        armor_img = armor['image'][0]
        weapon_img = weapon['image'][0]
        armor_label = armor['label'][0]
        weapon_label = weapon['label'][0] 

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
        with stat_cols[1]:
            st.write('### Enemy stats')
        with stat_cols[2]:
            st.write('### Events')
            self._event_placeholder = st.container(border=True)
        st.write('## My Inventory')
        self._render_inventory(player)
    
    def _new_event(self, placeholder, event: str):
        with placeholder:
            st.write(event)
            st.divider()
    
    def _render_inventory(self, player: Player) -> None:
        inv = player.inv
        inv_row = st.columns(len(inv))
        for ind, item in enumerate(inv):            
            with inv_row[ind]:
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
        self._new_event(self._event_placeholder,
                        f'Tried to use: {item['label'][0]}')
        print(f'Used item with uri: {uri}')
        player.item_use(ind, uri)      


view = MainGameView()
view.run()
