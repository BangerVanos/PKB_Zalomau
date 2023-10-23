from app.model.models import create_position
from app.model.models import create_department
from app.model.models import create_employee
from app.model.models import edit_employee
from app.model.models import delete_employee
from app.model.models import delete_employees
from app.db.db import initialize_engine
from app.model.models import fetch_positions_by_cipher_name
from app.model.models import fetch_department_by_name
from app.model.models import fetch_position_by_cipher_name
from app.model.models import fetch_only_position_by_id
from app.model.models import fetch_only_department_by_id
from app.model.models import Gender, FamilyStatus
from app.model.models import delete_history_records
import streamlit as st


def submit_position_creation():
    engine = initialize_engine()
    config = {'name': st.session_state['position_full_name'],
              'short_name': st.session_state['position_short_name'],
              'cipher_name': st.session_state['position_cipher_name'],
              'lowest_category': st.session_state['position_lowest_category'],
              'highest_category': st.session_state['position_highest_category']}
    create_position(engine, config)


def submit_department_creation():
    engine = initialize_engine()
    config = {'name': st.session_state['department_name'],
              'positions': fetch_positions_by_cipher_name(engine, st.session_state['department_positions'])}
    create_department(engine, config)


def submit_employee_creation():
    engine = initialize_engine()
    department = fetch_department_by_name(engine, st.session_state['employee_department'])
    position = fetch_position_by_cipher_name(engine, st.session_state['employee_position'])
    department = fetch_only_department_by_id(engine, department.id)
    position = fetch_only_position_by_id(engine, position.id)
    gender = {'Мужской': Gender.male,
              'Женский': Gender.female,
              'Другой': Gender.other}[st.session_state['employee_gender']]
    family_status = {'Женат/Замужем': FamilyStatus.married,
                     'Холост/Не замужем': FamilyStatus.not_married}[st.session_state['employee_family_status']]
    config = {'first_name': st.session_state['employee_first_name'],
              'last_name': st.session_state['employee_last_name'],
              'patronymic_name': st.session_state['employee_patronymic_name'],
              'birthday_date': st.session_state['employee_birthday_date'],
              'gender': gender,
              'family_status': family_status,
              'department': department,
              'position': position,
              'category': st.session_state['employee_category']}
    create_employee(engine, config)


def submit_employee_edit(employee_id: int):
    engine = initialize_engine()
    department = fetch_department_by_name(engine, st.session_state['edit_employee_department'])
    position = fetch_position_by_cipher_name(engine, st.session_state['edit_employee_position'])
    department = fetch_only_department_by_id(engine, department.id)
    position = fetch_only_position_by_id(engine, position.id)
    gender = {'Мужской': Gender.male,
              'Женский': Gender.female,
              'Другой': Gender.other}[st.session_state['edit_employee_gender']]
    family_status = {'Женат/Замужем': FamilyStatus.married,
                     'Холост/Не замужем': FamilyStatus.not_married}[st.session_state['edit_employee_family_status']]
    config = {'first_name': st.session_state['edit_employee_first_name'],
              'last_name': st.session_state['edit_employee_last_name'],
              'patronymic_name': st.session_state['edit_employee_patronymic_name'],
              'birthday_date': st.session_state['edit_employee_birthday_date'],
              'gender': gender,
              'family_status': family_status,
              'department': department,
              'position': position,
              'category': st.session_state['edit_employee_category']}
    edit_employee(engine, employee_id, config)


def submit_delete_employee(employee_id: int):
    engine = initialize_engine()
    delete_employee(engine=engine, employee_id=employee_id)


def submit_delete_employees(employee_ids: list[int]):
    engine = initialize_engine()
    delete_employees(engine=engine, employee_ids=employee_ids)


def submit_delete_records(record_ids: list[int]):
    engine = initialize_engine()
    delete_history_records(engine=engine, record_ids=record_ids)
