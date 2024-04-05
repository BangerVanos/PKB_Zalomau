import streamlit as st
from st_pages import Page, show_pages, Section


class WelcomeView:

    def __init__(self) -> None:
        st.set_page_config(page_title='Welcome!', layout='wide')
        show_pages([
            Page('app.py', name='Welcome page', icon='🚪'),
            Section(name='Projects section', icon='📜'),
            Page('app/frontend/load_projects_view.py',
                 name='Load and observe projects', icon='📖'),
            Page('app/frontend/create_project_view.py',
                 name='Create new project', icon='🛠'),
            Section(name='Developer Tools', icon='📜'),
            Page('app/frontend/execute_raw_sparql.py',
                 name='Execute SPARQL', icon='📐'),
        ])
    
    def run(self) -> None:
        pass


view = WelcomeView()
view.run()
