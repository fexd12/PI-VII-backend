from flask import Flask,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config,ProductionConfig
from flask_cors import CORS,cross_origin

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config_class = Config):
    app = Flask(__name__)
    # app.config.from_object(ProductionConfig)
    app.config.from_object(config_class)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)

    from app.api.usuario import bp as usuario_bp
    app.register_blueprint(usuario_bp,url_prefix='/usuario')

    from app.api.login import bp as login_bp
    app.register_blueprint(login_bp,url_prefix='/login')

    from app.api.envio import bp as envio_bp
    app.register_blueprint(envio_bp,url_prefix='/envio')

    from app.api.separacao import bp as separacao_bp
    app.register_blueprint(separacao_bp,url_prefix='/separacao')

    from app.api.pedidos import bp as pedidos_bp
    app.register_blueprint(pedidos_bp,url_prefix='/pedidos')

    return app

import app.models
