import streamlit as st
from st_pages import Page, show_pages
from app.backend.load_ontology import LoadOntology
from app.backend.fetch_from_onto import JSONFetcher
import owlready2 as owl


class WelcomeView:

    def __init__(self) -> None:
        st.set_page_config(page_title='Welcome to game!',
                           layout='wide')
        show_pages(
            [
                Page(path='app.py', name='Welcome!', icon='🤛'),
                Page(path='app/frontend/select_character_view.py',
                    name='Select character for game', icon='🧍'),
                Page(path='app/frontend/main_game_view.py',
                    name='Play', icon='🎮'),
                Page(path='app/frontend/add_new_item.py',
                    name='Add new item', icon='🗡️')
            ]
        )

    def run(self) -> None:        
        st.info('# Welcome to game!')


view = WelcomeView()
view.run()
