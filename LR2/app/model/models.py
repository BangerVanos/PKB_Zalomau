from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, SmallInteger, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
import datetime


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = 'department'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class Schedule(Base):
    __tablename__ = 'schedule'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    positions: Mapped[list['DepPosAssociation'] | None] = relationship(
        back_populates='department'
    )


class Position(Base):

    __tablename__ = 'position'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    short_name: Mapped[str] = mapped_column(String(15), unique=True)
    cipher_name: Mapped[str] = mapped_column(String(5), unique=True, nullable=False)
    lowest_category: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    highest_category: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    departments: Mapped[list['DepPosAssociation'] | None] = relationship(
        back_populates='position'
    )

    employees: Mapped[list['Employee'] | None] = relationship(
        back_populates='position'
    )


class DepPosAssociation(Base):
    __tablename__ = 'department_position_association'

    position_id: Mapped[int] = mapped_column(ForeignKey('position.id'), primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id'), primary_key=True)
    positions_amount: Mapped[int] = mapped_column(nullable=False)

    position: Mapped['Position'] = relationship(back_populates='departments')
    department: Mapped['Department'] = relationship(back_populates='positions')


class Employee(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic_name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    gender: Mapped[str] = mapped_column(String(6), nullable=False)
    family_status: Mapped[str] = mapped_column(String(50))
    category: Mapped[int] = mapped_column(SmallInteger)

    position: Mapped['Position'] = relationship(
        back_populates='employees'
    )


class History(Base):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int | None] = mapped_column(ForeignKey('employee.id'))
    from_department_id: Mapped[int | None] = mapped_column(ForeignKey('department.id'))
    to_department_id: Mapped[int | None] = mapped_column(ForeignKey('department.id'))
    from_position_id: Mapped[int | None] = mapped_column(ForeignKey('position.id'))
    to_position_id: Mapped[int | None] = mapped_column(ForeignKey('position.id'))
    from_category: Mapped[int | None] = mapped_column(SmallInteger)
    to_category: Mapped[int | None] = mapped_column(SmallInteger)
    start_date: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    finish_date: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
