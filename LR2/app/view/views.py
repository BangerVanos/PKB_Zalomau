import datetime

import streamlit as st
from .model_interaction import submit_position_creation
from .model_interaction import submit_department_creation
from .model_interaction import submit_employee_creation
from .model_interaction import submit_delete_employees
from .model_interaction import submit_employee_edit
from .model_interaction import submit_delete_records
from ..model.models import fetch_all_positions
from ..model.models import fetch_all_departments
from ..model.models import fetch_history
from ..model.models import fetch_department_by_name
from ..model.models import fetch_position_by_cipher_name
from ..model.models import fetch_only_department_by_id
from ..model.models import fetch_only_position_by_id
from ..model.models import fetch_employee_by_id
from ..model.models import fetch_employees
from ..model.models import Gender, FamilyStatus, WorkStatus
from ..db.db import initialize_engine


def main_page():
    st.set_page_config(page_title='БД предприятия', layout='wide')
    st.write('## Главная страница, откуда можно отправиться куда угодно')


def add_position_page():
    st.set_page_config(page_title='Добавить новую должность', layout='wide')
    st.write('## Добавить должность')
    st.text_input('Полное название должности', placeholder='Введите полное название должности сюда...',
                  key='position_full_name', max_chars=50)
    st.text_input('Краткое название должности', placeholder='Введите краткое название должности сюда...',
                  key='position_short_name', max_chars=15)
    st.text_input('Шифр должности', placeholder='Введите полное название должности сюда...',
                  key='position_cipher_name', max_chars=5)
    st.number_input('Нижняя категория', min_value=1, max_value=18, key='position_lowest_category')
    st.number_input('Верхняя категория', min_value=1, max_value=18, key='position_highest_category')
    st.button('Добавить новую должность', on_click=submit_position_creation)


def lookup_all_positions_page():
    st.set_page_config(page_title='Просмотр всех должностей на предприятии', layout='wide')
    st.write('## Все должности предприятия')
    positions = fetch_all_positions(engine=initialize_engine())
    columns = st.columns(5)
    with columns[0]:
        st.write('*Название должности*')
    with columns[1]:
        st.write('*Краткое название должности*')
    with columns[2]:
        st.write('*Шифр должности*')
    with columns[3]:
        st.write('*Низшая категория*')
    with columns[4]:
        st.write('*Высшая категория*')
    for position in positions:
        with columns[0]:
            st.write(position.name)
        with columns[1]:
            st.write(position.short_name)
        with columns[2]:
            st.write(position.cipher_name)
        with columns[3]:
            st.write(position.lowest_category)
        with columns[4]:
            st.write(position.highest_category)


def add_department_page():
    st.set_page_config(page_title='Добавление подразделения', layout='wide')
    st.write('## Добавить подразделение')
    st.text_input('Название подразделения', placeholder='Введите название подразделения сюда', max_chars=100,
                  key='department_name')
    st.multiselect('Выберите должности данного подразделения',
                   options=[position.cipher_name for position in fetch_all_positions(engine=initialize_engine())],
                   key='department_positions')
    st.button('Добавить новое подразделение', on_click=submit_department_creation)


def lookup_all_departments_page():
    st.set_page_config(page_title='Просмотр подразделений', layout='wide')
    st.write('## Все подразделения предприятия')
    departments = fetch_all_departments(engine=initialize_engine())
    columns = st.columns(2)
    with columns[0]:
        st.write('*Название подразделения*')
    with columns[1]:
        st.write('*Должности данного подразделения*')
    for department in departments:
        with columns[0]:
            st.write(department.name)
        with columns[1]:
            st.selectbox('Должности', options=[position.name for position in department.positions])


def add_employee_page():
    st.set_page_config(page_title='Добавить нового сотрудника', layout='wide')
    st.write('## Добавить нового сотрудника')
    st.text_input('Фамилия сотрудника', key='employee_last_name', max_chars=50)
    st.text_input('Имя сотрудника', key='employee_first_name', max_chars=50)
    st.text_input('Отчество сотрудника', key='employee_patronymic_name', max_chars=50)
    st.date_input('Возраст сотрудника', key='employee_birthday_date', value=None,
                  min_value=datetime.date(datetime.datetime.now().year - 100, 1, 1),
                  max_value=datetime.date(datetime.datetime.now().year + 100, 12, 31))
    st.selectbox('Пол сотрудника', key='employee_gender', options=['Мужской', 'Женский', 'Другой'])
    st.selectbox('Семейный статус', key='employee_family_status', options=['Женат/Замужем', 'Холост/Не замужем'])
    engine = initialize_engine()
    departments = fetch_all_departments(engine)
    dep_select = st.selectbox('Подразделение', key='employee_department', placeholder='Выберите подразделение...',
                              options=[department.name for department in departments],
                              index=None)
    if dep_select:
        department = fetch_department_by_name(engine, st.session_state['employee_department'])
        pos_select = st.selectbox('Должность', key='employee_position', placeholder='Выберите должность...',
                                  options=[position.cipher_name for position in department.positions],
                                  index=None)
        if pos_select:
            position = fetch_position_by_cipher_name(engine, st.session_state['employee_position'])
            st.slider('Категория', position.lowest_category, position.highest_category,
                      position.lowest_category, key='employee_category')
    st.button('Добавить нового сотрудника', on_click=submit_employee_creation)


def lookup_all_employees():
    st.set_page_config(page_title='Все сотрудники', layout='wide')
    st.write('## Все сотрудники')
    genders = {Gender.male: 'Мужской', Gender.female: 'Женский', Gender.other: 'Другой'}
    family_status = {FamilyStatus.married: 'Женат/Замужем', FamilyStatus.not_married: 'Холост/Не замужем'}
    st.session_state.employees_to_delete = []
    columns = st.columns(11)
    columns_names = ['*Фамилия*', '*Имя*', '*Отчество*', '*Дата рождения*', '*Пол*', '*Семейный статус*',
                     '*Подразделение*', '*Должность*', '*Категория*', '*Выбрать*', '*Изменить*']
    for i in range(len(columns)):
        with columns[i]:
            st.write(columns_names[i])
    filter_employees()
    placeholder = st.empty()
    with placeholder.container():
        for employee in st.session_state.employees:
            with st.container():
                columns = st.columns(11)
                with columns[0]:
                    st.write(employee.last_name)
                with columns[1]:
                    st.write(employee.first_name)
                with columns[2]:
                    st.write(employee.patronymic_name)
                with columns[3]:
                    st.write(employee.birthday_date)
                with columns[4]:
                    st.write(genders[employee.gender])
                with columns[5]:
                    st.write(family_status[employee.family_status])
                with columns[6]:
                    st.write('Нет' if employee.department is None else employee.department.name)
                with columns[7]:
                    st.write('Нет' if employee.position is None else employee.position.name)
                with columns[8]:
                    st.write(employee.category)
                with columns[9]:
                    chkbox = st.checkbox('Выбрать', key=f'check_employee_{employee.id}', label_visibility='hidden')
                    if chkbox:
                        st.session_state.employees_to_delete.append(employee.id)
                with columns[10]:
                    edit_button = st.button('⚙️', key=f'edit_employee_{employee.id}')
                    if edit_button:
                        st.session_state.edit_employee_id = employee.id
                        st.write(st.session_state.edit_employee_id)

    with st.sidebar:
        st.text_input('Отфильтровать по фамилии', key='employee_filter_last_name', max_chars=50,
                      on_change=filter_employees)
        st.text_input('Отфильтровать по имени', key='employee_filter_first_name', max_chars=50,
                      on_change=filter_employees)
        st.text_input('Отфильтровать по отчеству', key='employee_filter_patronymic_name', max_chars=50,
                      on_change=filter_employees)
        st.selectbox('Отфильтровать по должности',
                     options=[position.cipher_name for position in fetch_all_positions(engine=initialize_engine())],
                     key='employee_filter_position', index=None,
                     on_change=filter_employees)
        st.number_input('Отфильтровать по возрасту меньше указанного', key='employee_filter_age',
                        max_value=120, min_value=15, value=120,
                        on_change=filter_employees)
        st.checkbox('Женщины пенсионного возраста?', key='employee_filter_retired_age',
                    on_change=filter_employees)
        st.button('Очистить все фильтры', key='clear_filters',
                  on_click=clear_filters)

        button = st.button('🗑️ Удалить выбранных сотрудников', key='delete_employees')
        if button:
            st.write()
            submit_delete_employees(employee_ids=st.session_state.employees_to_delete)
            st.rerun()

    if st.session_state.get('edit_employee_id'):
        genders = {Gender.male: 'Мужской', Gender.female: 'Женский', Gender.other: 'Другой'}
        family_status = {FamilyStatus.married: 'Женат/Замужем', FamilyStatus.not_married: 'Холост/Не замужем'}
        engine = initialize_engine()
        employee = fetch_employee_by_id(engine, st.session_state.edit_employee_id)
        st.info('Редактирование информации о сотруднике сотрудника')
        st.text_input('Фамилия', max_chars=50, value=employee.last_name,
                      key='edit_employee_last_name')
        st.text_input('Имя', max_chars=50, value=employee.first_name,
                      key='edit_employee_first_name')
        st.text_input('Отчество', max_chars=50, value=employee.patronymic_name,
                      key='edit_employee_patronymic_name')
        st.date_input('Дата рождения', value=employee.birthday_date,
                      key='edit_employee_birthday_date',
                      min_value=datetime.date(datetime.datetime.now().year - 100, 1, 1),
                      max_value=datetime.date(datetime.datetime.now().year + 100, 12, 31)
                      )
        gender_opts = ['Мужской', 'Женский', 'Другой']
        st.selectbox('Пол', options=gender_opts, index=gender_opts.index(genders[employee.gender]),
                     key='edit_employee_gender')
        family_status_opts = ['Женат/Замужем', 'Холост/Не замужем']
        st.selectbox('Семейный статус', options=['Женат/Замужем', 'Холост/Не замужем'],
                     index=family_status_opts.index(family_status[employee.family_status]),
                     key='edit_employee_family_status')
        departments = fetch_all_departments(engine)
        department_opts = [department.name for department in departments]
        department_value = department_opts.index(employee.department.name)
        st.selectbox('Подразделение', options=department_opts,
                     index=department_value,
                     key='edit_employee_department')
        department = fetch_department_by_name(engine, st.session_state['edit_employee_department'])
        position_opts = [position.cipher_name for position in department.positions]
        position_value = position_opts.index(employee.position.cipher_name)
        st.selectbox('Должность', key='edit_employee_position',
                     options=position_opts, index=position_value
                     )
        position = fetch_position_by_cipher_name(engine, st.session_state['edit_employee_position'])
        st.slider('Категория', position.lowest_category, position.highest_category,
                  value=employee.category, key='edit_employee_category', )
        columns = st.columns(2)
        with columns[0]:
            st.button('Отредактировать информацию 🔄',
                      on_click=lambda: submit_employee_edit(st.session_state.edit_employee_id))
        with columns[1]:
            st.button('Отмена ❌', on_click=clear_edit_employee_id)
    else:
        st.info('## Вы можете выбрать сотрудника для редактирования на этой странице!\n'
                '### Для выбора нажмите ⚙️ напротив нужного сотрудника')


def filter_employees():
    engine = initialize_engine()
    employee_filters = {}
    if st.session_state.get('employee_filter_last_name'):
        employee_filters['last_name'] = st.session_state.employee_filter_last_name
    if st.session_state.get('employee_filter_first_name'):
        employee_filters['first_name'] = st.session_state.employee_filter_first_name
    if st.session_state.get('employee_filter_patronymic_name'):
        employee_filters['patronymic_name'] = st.session_state.employee_filter_patronymic_name
    if st.session_state.get('employee_filter_position'):
        position_id = fetch_position_by_cipher_name(engine=engine,
                                                    cipher_name=st.session_state.employee_filter_position).id
        employee_filters['position'] = position_id
    if st.session_state.get('employee_filter_age'):
        employee_filters['age'] = st.session_state.employee_filter_age
    if st.session_state.get('employee_filter_retired_age'):
        employee_filters['retired_age'] = True
    st.session_state.employees = fetch_employees(engine=engine, filters=employee_filters)


def clear_filters():
    st.session_state.employee_filter_last_name = None
    st.session_state.employee_filter_first_name = None
    st.session_state.employee_filter_patronymic_name = None
    st.session_state.employee_filter_position = None
    st.session_state.employee_filter_age = 120
    st.session_state.employee_filter_retired_age = False
    st.session_state.employees = fetch_employees(engine=initialize_engine(), filters=dict())


def clear_edit_employee_id():
    if st.session_state.get('edit_employee_id'):
        st.session_state.edit_employee_id = None


def lookup_history_page():
    st.set_page_config(page_title='История сотрудников', layout='wide')
    st.session_state.records_to_delete = []
    columns_names = ['*ФИО сотрудника*', '*Подразделение*', '*Должность*', '*Категория*', '*Статус*',
                     '*Дополнительная информация*', '*Дата*', '*Выбрать*']
    columns = st.columns(8)
    for i in range(len(columns)):
        with columns[i]:
            st.write(columns_names[i])
    engine = initialize_engine()
    history_records = fetch_history(engine)
    placeholder = st.empty()
    with placeholder.container():
        for record in history_records:
            with st.container():
                with columns[0]:
                    st.write(record.employee_name)
                with columns[1]:
                    department = fetch_only_department_by_id(engine, record.department_id)
                    st.write(department.name)
                with columns[2]:
                    position = fetch_only_position_by_id(engine, record.position_id)
                    st.write(position.name)
                with columns[3]:
                    st.write(str(record.category))
                with columns[4]:
                    if record.status == WorkStatus.hired:
                        st.markdown(':green[НАНЯТ]')
                    elif record.status == WorkStatus.fired:
                        st.markdown(':red[УВОЛЕН]')
                    elif record.status == WorkStatus.moved:
                        st.markdown(':blue[ПЕРЕМЕЩЁН]')
                    elif record.status == WorkStatus.change_category:
                        st.markdown(':yellow[ИЗМЕНЕНА КАТЕГОРИЯ]')
                    else:
                        st.write('НЕИЗВЕСТНО')
                with columns[5]:
                    st.write(str(record.additional_info))
                with columns[6]:
                    st.write(str(record.record_date))
                with columns[7]:
                    chkbox = st.checkbox('Выбрать', key=f'check_employee_{record.id}', label_visibility='hidden')
                    if chkbox:
                        st.session_state.records_to_delete.append(record.id)
    with st.sidebar:
        button = st.button('🗑️ Удалить выбранные записи', key='delete_records')
        if button:
            submit_delete_records(st.session_state.records_to_delete)
            st.rerun()




