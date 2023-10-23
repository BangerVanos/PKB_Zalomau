import enum
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload
import datetime


class FamilyStatus(enum.Enum):
    married = 'married'
    not_married = 'not_married'


class Gender(enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'


class WorkStatus(enum.Enum):
    hired = 'hired'
    fired = 'fired'
    moved = 'moved'
    change_category = 'changed_category'


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = 'department'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    employees: Mapped[list['Employee'] | None] = relationship(
        back_populates='department'
    )

    positions: Mapped[list['Position'] | None] = relationship(
        back_populates='departments', secondary='department_position_association'
    )

    positions_associations: Mapped[list['DepPosAssociation'] | None] = relationship(
        back_populates='department_assoc'
    )

    def __repr__(self):
        return f'Department(id={self.id}, name={self.name})'

    def __str__(self):
        return self.__repr__()


class Position(Base):
    __tablename__ = 'position'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    short_name: Mapped[str] = mapped_column(String(15), unique=True)
    cipher_name: Mapped[str] = mapped_column(String(5), unique=True, nullable=False)
    lowest_category: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    highest_category: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    departments: Mapped[list['Department'] | None] = relationship(
        back_populates='positions', secondary='department_position_association'
    )

    departments_associations: Mapped[list['DepPosAssociation'] | None] = relationship(
        back_populates='position_assoc'
    )

    employees: Mapped[list['Employee'] | None] = relationship(
        back_populates='position'
    )

    def __repr__(self):
        return f'Position(id={self.id}, name={self.name}, short_name={self.short_name}, ' \
               f'cipher_name={self.cipher_name}, lowest_category={self.lowest_category}, ' \
               f'highest_category={self.highest_category})'

    def __str__(self):
        return self.__repr__()


class DepPosAssociation(Base):
    __tablename__ = 'gen'

    position_id: Mapped[int] = mapped_column(ForeignKey('position.id', ondelete='CASCADE'), primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id', ondelete='CASCADE'), primary_key=True)
    positions_amount: Mapped[int | None] = mapped_column(SmallInteger)

    position_assoc: Mapped['Position'] = relationship(back_populates='departments_associations')
    department_assoc: Mapped['Department'] = relationship(back_populates='positions_associations')


class Employee(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic_name: Mapped[str] = mapped_column(String(50))
    birthday_date: Mapped[datetime.date] = mapped_column()
    gender: Mapped[Gender]
    family_status: Mapped[FamilyStatus]

    department: Mapped['Department'] = relationship(
        back_populates='employees'
    )
    department_id: Mapped[int | None] = mapped_column(ForeignKey('department.id', ondelete='SET NULL'))

    position_id: Mapped[int | None] = mapped_column(ForeignKey('position.id', ondelete='SET NULL'))
    position: Mapped['Position'] = relationship(
        back_populates='employees'
    )

    category: Mapped[int] = mapped_column(SmallInteger)

    def __repr__(self):
        return f'Employee(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, ' \
               f'patronymic_name={self.patronymic_name}, birthday={self.birthday_date}, gender={self.gender}, ' \
               f'family_status={self.family_status}, category={self.category})'

    def __str__(self):
        return self.__repr__()


class History(Base):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_name: Mapped[int | None] = mapped_column(String)
    department_id: Mapped[int | None] = mapped_column(ForeignKey('department.id', ondelete='SET NULL'))
    position_id: Mapped[int | None] = mapped_column(ForeignKey('position.id', ondelete='SET NULL'))
    category: Mapped[int | None] = mapped_column(SmallInteger)
    additional_info: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[WorkStatus]
    record_date: Mapped[datetime.datetime | None] = mapped_column(server_default=func.now())


def create_employee(engine: sqlalchemy.Engine, config: dict):
    """INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    with Session(engine) as session:
        new_employee = Employee(
            first_name=config['first_name'],
            last_name=config['last_name'],
            patronymic_name=config['patronymic_name'],
            birthday_date=config['birthday_date'],
            gender=config['gender'],
            family_status=config['family_status'],
            department=config['department'],
            position=config['position'],
            category=config['category']
        )
        session.add(new_employee)
        session.commit()
        hist_config = {'employee_name': f'{config["last_name"]} {config["first_name"]} {config["patronymic_name"]}',
                       'department_id': new_employee.department.id,
                       'position_id': new_employee.position.id,
                       'category': config['category'],
                       'status': WorkStatus.hired}
    write_to_history(engine, hist_config)


def edit_employee(engine: sqlalchemy.Engine, employee_id: int, config: dict):
    with Session(engine) as session:
        stmt = select(Employee).where(Employee.id == employee_id)
        employee = session.scalar(stmt)
        employee.first_name = config['first_name']
        employee.last_name = config['last_name']
        employee.patronymic_name = config['patronymic_name']
        employee.birthday_date = config['birthday_date']
        employee.gender = config['gender']
        employee.family_status = config['family_status']
        employee.department = config['department']
        employee.position = config['position']
        employee.category = config['category']
        session.commit()
        hist_config = {'employee_name': f'{config["last_name"]} {config["first_name"]} {config["patronymic_name"]}',
                       'department_id': employee.department.id,
                       'position_id': employee.position.id,
                       'category': config['category'],
                       'status': WorkStatus.moved
                       }
    write_to_history(engine, hist_config)


def fetch_employee_by_id(engine: sqlalchemy.Engine, employee_id: int):
    with Session(engine) as session:
        stmt = select(Employee).where(Employee.id == employee_id)\
            .options(joinedload(Employee.department)).options(joinedload(Employee.position))
        employee = session.scalar(stmt)
    return employee


def fetch_all_employees(engine: sqlalchemy.Engine):
    """SELECT * FROM employees"""
    with Session(engine) as session:
        stmt = select(Employee).options(joinedload(Employee.department)).options(joinedload(Employee.position))
        employees = session.scalars(stmt).unique().all()
    return employees


def fetch_employees(engine: sqlalchemy.Engine, filters: dict):
    with Session(engine) as session:
        stmt = select(Employee).options(joinedload(Employee.department)).options(joinedload(Employee.position))
        if filters.get('first_name'):
            stmt = stmt.where(Employee.first_name.contains(filters['first_name']))
        if filters.get('last_name'):
            stmt = stmt.where(Employee.last_name.contains(filters['last_name']))
        if filters.get('patronymic_name'):
            stmt = stmt.where(Employee.patronymic_name.contains(filters['patronymic_name']))
        if filters.get('retired_age'):
            stmt = stmt.where(Employee.gender == Gender.female,
                              (func.julianday("now") - func.julianday(Employee.birthday_date) + 1) / 365 >= 58)
        if filters.get('age'):
            stmt = stmt.where((func.julianday("now") - func.julianday(Employee.birthday_date) + 1) / 365
                              < filters['age'])
        if filters.get('position'):
            stmt = stmt.where(Employee.position_id == filters['position'])
        employees = session.scalars(stmt).unique().all()
    return employees


def delete_employee(engine: sqlalchemy.Engine, employee_id: int):
    with Session(engine) as session:
        employee = session.query(Employee).where(Employee.id == employee_id).first()
        stmt = delete(Employee).where(Employee.id == employee_id)
        session.execute(stmt)
        session.commit()
    hist_config = {'employee_name': f'{employee.last_name} {employee.first_name} {employee.patronymic_name}',
                   'department_id': employee.department_id,
                   'position_id': employee.position_id,
                   'category': employee.category,
                   'status': WorkStatus.fired
                   }
    write_to_history(engine, hist_config)


def delete_employees(engine: sqlalchemy.Engine, employee_ids: list):
    with Session(engine) as session:
        deleted_employees = session.query(Employee).where(Employee.id.in_(employee_ids)).all()
        stmt = delete(Employee).where(Employee.id.in_(employee_ids))
        session.execute(stmt)
        session.commit()
    for employee in deleted_employees:
        hist_config = {'employee_name': f'{employee.last_name} {employee.first_name} {employee.patronymic_name}',
                       'department_id': employee.department_id,
                       'position_id': employee.position_id,
                       'category': employee.category,
                       'status': WorkStatus.fired
                       }
        write_to_history(engine, hist_config)


def create_position(engine: sqlalchemy.Engine, config: dict):
    with Session(engine) as session:
        new_position = Position(
            name=config['name'],
            short_name=config['short_name'],
            cipher_name=config['cipher_name'],
            lowest_category=config['lowest_category'],
            highest_category=config['highest_category']
        )
        session.add(new_position)
        session.commit()


def fetch_all_positions(engine: sqlalchemy.Engine):
    """SELECT * FROM positions"""
    with Session(engine) as session:
        stmt = select(Position)
        positions = session.scalars(stmt).all()
    return positions


def fetch_positions_by_cipher_name(engine: sqlalchemy.Engine, cipher_names: list):
    with Session(engine) as session:
        stmt = select(Position).where(Position.cipher_name.in_(cipher_names))
        positions = session.scalars(stmt).all()
    return positions


def fetch_position_by_cipher_name(engine: sqlalchemy.Engine, cipher_name: str):
    with Session(engine) as session:
        stmt = select(Position).where(Position.cipher_name == cipher_name)
        position = session.scalar(stmt)
    return position


def create_department(engine: sqlalchemy.Engine, config: dict):
    with Session(engine) as session:
        new_department = Department(
            name=config['name'],
            positions=config['positions']
        )
        session.add(new_department)
        session.commit()


def fetch_all_departments(engine: sqlalchemy.Engine):
    with Session(engine) as session:
        stmt = select(Department).options(joinedload(Department.positions))
        departments = session.scalars(stmt).unique().all()
    return departments


def fetch_department_by_name(engine: sqlalchemy.Engine, name: str):
    with Session(engine) as session:
        stmt = select(Department).where(Department.name == name).options(selectinload(Department.positions))
        department = session.scalar(stmt)
    return department


def fetch_only_department_by_id(engine: sqlalchemy.Engine, id_: int):
    with Session(engine) as session:
        stmt = select(Department).where(Department.id == id_)
        department = session.scalar(stmt)
    return department


def fetch_only_position_by_id(engine: sqlalchemy.Engine, id_: int):
    with Session(engine) as session:
        stmt = select(Position).where(Position.id == id_)
        position = session.scalar(stmt)
    return position


def write_to_history(engine: sqlalchemy.Engine, config: dict):
    with Session(engine) as session:
        history_record = History(
            employee_name=config['employee_name'],
            department_id=config['department_id'],
            position_id=config['position_id'],
            category=config['category'],
            status=config['status']
        )
        if config.get('additional_info'):
            history_record.additional_info = config['additional_info']
        session.add(history_record)
        session.commit()


def fetch_history(engine: sqlalchemy.Engine):
    with Session(engine) as session:
        stmt = select(History)
        history_records = session.scalars(stmt).all()
    return history_records


def delete_history_records(engine: sqlalchemy.Engine, record_ids: list):
    with Session(engine) as session:
        stmt = delete(History).where(History.id.in_(record_ids))
        session.execute(stmt)
        session.commit()

