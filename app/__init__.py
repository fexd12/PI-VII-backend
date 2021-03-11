from flask import Flask,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS,cross_origin

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # app.redis = Redis.from_url(app.config['REDIS_URL'])
    # app.task_queue = rq.Queue('pi_task',connection=app.redis)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)

    from app.api.usuario import bp as usuario_bp
    app.register_blueprint(usuario_bp,url_prefix='/usuario')

    from app.api.login import bp as login_bp
    app.register_blueprint(login_bp,url_prefix='/login')
    
    from app.api.salas import bp as salas_bp
    app.register_blueprint(salas_bp,url_prefix='/salas')

    from app.api.tag import bp as tag_bp
    app.register_blueprint(tag_bp,url_prefix='/tag')

    from app.api.email import bp as email_bp
    app.register_blueprint(email_bp,url_prefix='/email')

    from app.api.agendamento import bp as agendamento_bp
    app.register_blueprint(agendamento_bp,url_prefix='/agendamento')

    return app

import app.models
