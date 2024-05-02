import streamlit as st
from app.backend.fetch_from_onto import JSONFetcher
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
        character = self._fetcher.fetch_by_uri(uri)        

        stat_cols = st.columns([1, 1, 2])

        # Fetching player stats
        armor = self._fetcher.fetch_by_uri(str(character['equipped_armor'][0]))
        weapon = self._fetcher.fetch_by_uri(str(character['equipped_weapon'][0]))

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
            stat_row.metric(label='HP', value=character['hp'][0])
            stat_row.metric(label='AP', value=character['ap'][0])
            stat_row.metric(label='LVL', value=character['lvl'][0])
            stat_row.metric(label='XP', value=character['exp'][0])
        with stat_cols[1]:
            st.write('### Enemy stats')
        with stat_cols[2]:
            st.write('### Events')
            self._event_placeholder = st.container(border=True)
        st.write('## My Inventory')
        self._render_inventory(character)
    
    def _new_event(self, placeholder, event: str):
        with placeholder:
            st.write(event)
            st.divider()
    
    def _render_inventory(self, character: dict) -> None:
        inv = character['item_of_inv']
        inv_row = st.columns(len(inv))
        for ind, item_uri in enumerate(inv):
            item = self._fetcher.fetch_by_uri(str(item_uri))
            with inv_row[ind]:
                card(
                    title=item['label'][0],
                    image=item['image'][0],
                    text=item['label'][0],
                    on_click=(lambda ind=ind, uri=item_uri,
                            item=item: self._handle_item_click(ind, uri, item))
                )            
    
    def _handle_item_click(self, ind: int, uri: str, item: dict) -> None:
        self._new_event(self._event_placeholder,
                        f'Tried to use: {item['label'][0]}')        


view = MainGameView()
view.run()
