from sqlalchemy import create_engine
import app.config as cf
from app.model.models import Base


def initialize_engine():
    return create_engine(cf.DB_URL, echo=cf.SQL_ECHO)


def initialize_tables(engine):
    Base.metadata.create_all(bind=engine)
