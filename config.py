import os

BASE_DIR=os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI='sqlite:///{}'.format(os.path.join(BASE_DIR,'pybo.db'))
#데이터 베이스 접속 주소
SQLALCHEMY_TRACK_MODIFICATIONS=False
#SqlAlchemy의 이벤트를 처리하는 옵션. pybo.db라는 데이터베이스 파일을
#프로젝트의 루트 디렉토리에 저장하라는 뜻.
SECRET_KEY = "dev"
