from config.default import *

SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR,"pybo.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"