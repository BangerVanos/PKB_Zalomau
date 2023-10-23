import app.db.db as db
import app.config as cf
import streamlit as st


engine = db.initialize_engine()
db.initialize_tables(engine)
st.set_page_config(page_title='О приложении', layout='wide')
st.write('# Добро пожаловать!')
st.write('Это небольшое приложение для управления базой данных некоторого предприятия. Сделано '
         'в рамках курса ПБЗ (5 семестр). Лабораторная номер 2, вариант 7. Для навигации используйте меню слева')
