from flask import Flask
from flask_migrate import Migrate


migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)
    
    migrate.init_app(app=app, db=None, directory="./migrations")
    
    return app
