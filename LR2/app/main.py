import db.db as db
import config as cf
import flet as ft
from view.views import run_app


if __name__ == '__main__':
    print(cf.DB_URL)
    engine = db.initialize_engine()
    # db.initialize_tables(engine)
    ft.app(target=run_app)
