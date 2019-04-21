from flask import Flask
from app import api_bp
from model import db
from flask_jwt_extended import JWTManager


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

    app.register_blueprint(api_bp, url_prefix='/api')

    jwt = JWTManager(app)

    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)
