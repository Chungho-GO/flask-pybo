from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
# import config

# 함수명으로 create_app 대신 다른 이름을 사용하면 정상으로 동작하지 않는다.
# create_app은 플라스크 내부에서 정의된 함수명이다.

# 따라서 pybo.py 파일과 pybo/init.py 파일은 동일한 pybo 모듈을 구성하는 파일이므로,
# 이 두 파일 중 하나를 FLASK_APP 환경 변수에 지정하여도 Flask는 pybo 모듈을 찾아서 실행할 수 있습니다. 
# 이렇게 파일 이름을 바꾸어도 동작하는 이유는 Python 모듈 검색 경로에서 해당 모듈을 찾기 때문입니다.
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    # app.config.from_object(config)
    app.config.from_envvar('APP_CONFIG_FILE')
    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app,db, render_as_batch=True)
    else:
        migrate.init_app(app,db)
    
    
    from . import models

    # @app.route('/')
    # def hello_pybo():
    #     return 'Hello, Pybo!'
    
    # BluePrint
    from .views import main_views,question_views,answer_views,auth_views
    app.register_blueprint(main_views.bp)  
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # 오류 페이지
    app.register_error_handler(404, page_not_found)

    return app