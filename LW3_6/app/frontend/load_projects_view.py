import streamlit as st
from app.backend.load_projects import LoadProjects
from app.backend.ontology_loader import OntologyLoader
import owlready2 as owl


class LoadProjectsView:
    
    def __init__(self) -> None:
        st.session_state['ontology'] = None    

    def _load_ontology_on_start(self) -> owl.Ontology:
        if st.session_state['ontology'] is None:
            try:
                onto = OntologyLoader.load_ontology()
            except Exception as err:
                st.error(f'Error occured during loading an ontology: '
                        f'{err}!')
            else:
                return onto
        else:
            return st.session_state['ontology']

    def run(self) -> None:
        onto = self._load_ontology_on_start()
        projects = LoadProjects.load_projects(onto)
        for project in list(projects):
            st.write(project.label)
            


view = LoadProjectsView()
view.run()
