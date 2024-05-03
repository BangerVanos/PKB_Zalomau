import streamlit as st
from streamlit_extras.stateful_button import button
from app.backend.fetch_from_onto import JSONFetcher
from app.backend.add_new_individual import IndividualCreator


class SelectCharacterView:

    def __init__(self) -> None:
        self._fetcher = JSONFetcher()
        self._creator = IndividualCreator()
        st.set_page_config(layout='wide',
                           page_title='Select game character!')
        st.session_state['selected_character'] = None

    def run(self) -> None:
        characters = self._fetcher.fetch_all_characters()        
        st.write('## Select from available characters...')
        for character in characters:            
            self._render_character_cards(character)        
        st.write('## ...or create a new one!')      
        self._render_new_character()
        selected_uri = (None if (uri := st.session_state['selected_character'])
                        is None else uri.split('.')[-1].capitalize())
        st.info(f'## You\'ve selected: {selected_uri}')
    
    def _render_character_cards(self, character: dict):        
        selected_character = st.session_state['selected_character']        
        uri = character['uri']           
        class_label = self._fetcher.fetch_by_uri(
            str(character['character_class'][0])
        )['label']
        with st.expander(label=uri.split('.')[-1].capitalize()):
            armor_img = self._fetcher.fetch_by_uri(str(character['equipped_armor'][0]))['image'][0]
            weapon_img = self._fetcher.fetch_by_uri(str(character['equipped_weapon'][0]))['image'][0]            
            st.image(image=[armor_img, weapon_img],
                     caption=['Armor', 'Weapon'],
                     width=256)
            st.write(f'LVL: {character['lvl'][0]}')
            st.write(f'XP: {character['exp'][0]}')
            st.write(f'HP: {character['hp'][0]}')
            st.write(f'AP: {character['ap'][0]}')
            st.write(f'Class: {class_label}')
            is_already_selected: bool = selected_character == uri
            select_btn = st.button(label='Select' if not is_already_selected else 'Selected!',
                                   key=f'select_{uri}',
                                   disabled=is_already_selected)
            delete_btn = st.button(
                label='Delete character',
                key=f'delete_{uri}',
                disabled=is_already_selected
            )
            if select_btn:
                st.session_state['selected_character'] = uri
                st.session_state['player'] = None
            if delete_btn:
                st.session_state['selected_character'] = None
                self._creator.destroy_individual(uri)
                st.rerun()          

    def _render_new_character(self) -> None:
        classes = self._fetcher.fetch_all_character_classes()        
        labels = {ch_cls['uri']: ch_cls['label'][0] for ch_cls in classes}
        uris = list(labels.keys())        
        st.write('Select character class')
        cls_selection = st.selectbox(label='Select class',
                                     options=uris,
                                     format_func=lambda opt: labels[opt],
                                     key='new_character_class')
        if cls_selection:
            selected = self._fetcher.fetch_by_uri(cls_selection)
            st.info(f'HP: {selected.get('base_hp', [100])[0]}\n'
                    f'AP: {selected.get('base_ap', [150])[0]}\n')
            select_btn = st.button(
                label='Create!',
                key='new_character_btn',
                on_click=lambda: self._create_new_character(selected['uri'])
            )
    
    def _create_new_character(self, uri: str) -> None:
        st.session_state['selected_character'] = uri
        st.session_state['player'] = None
        self._creator.create_new_character(uri)
              


view = SelectCharacterView()
view.run()
