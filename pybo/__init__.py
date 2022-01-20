import imp
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
from pybo.filter import format_datetime
from sqlalchemy import MetaData
from flaskext.markdown import Markdown



naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app():
    app=Flask(__name__)
    app.config.from_object(config) #config.py파일에 작성한 항목을 app.config 환경변수로
                                   #부르기 위해서 코드를 추가함.
    #ORM
    db.init_app(app) 
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app,db,render_as_batch=True)                               #전역변수로 db,migrate 객체를 만든 다음 init_app 메서드를
    else:                                                                           #이용해 초기화함.
        migrate.init_app(app,db)                                                 
    from . import models
    
    #Blueprint
    from .views import question_views,main_views,answer_views,auth_views,comment_views,vote_views
    app.register_blueprint(question_views.bp)
    app.register_blueprint(main_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)
    
    #filter
    from .filter import format_datetime
    app.jinja_env.filters['datetime']=format_datetime
    
    #markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])


    return app
