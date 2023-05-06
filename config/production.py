from config.default import *

SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR,"pybo.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x08a\t\x14\x17\x04\xf1\x90\xaf\xb7@\xdfGizw'