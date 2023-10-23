import os


SQL_ECHO = True
DB_NAME = 'facility.db'
DB_PATH = '/' + os.path.realpath(os.path.join(__file__, '..', DB_NAME))
DB_ENGINE = 'sqlite://'
DB_URL = DB_ENGINE + DB_PATH

WEB_URL = 'localhost:8501'
