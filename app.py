from flask import Flask, render_template
from flask_restx import Api

from config import Config

from setup_db import db
from utils import create_data
from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns

api = Api(title="Flask Course Project 4", doc="/docs")  # fr


# функция создания основного объекта app
def create_app(config: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)  # fr
    app.app_context().push()

    @app.route('/')  # fr
    def index():
        return render_template('index.html')

    api.init_app(app)  # fr

    return app


# функция подключения расширений
def register_extensions(app: Flask):
    db.init_app(app)
    # api = Api(app, title="Flask Course Project 4", description='Movies API')  # fr del
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    # create_data(app, db)


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)

    # register_extensions(app)  # fr del

    app.run(host='127.0.0.1', port=25000)
