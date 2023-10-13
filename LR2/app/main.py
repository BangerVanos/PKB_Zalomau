import db.db as db
import config as cf
from view.views import App


if __name__ == '__main__':
    print(cf.DB_URL)
    engine = db.initialize_engine()
    # db.initialize_tables(engine)
    app = App()
    app.mainloop()
