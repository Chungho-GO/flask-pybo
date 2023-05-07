from config.default import *
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters':{
        'defalut' : {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    
    },

    'handlers':{
        'file' : {
            'level':'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/myproject.log'),
            'maxBytes': 1024 * 1024 * 5 ,
            'backupCount' : 5,
            'formatter' : 'default',
        },
    },
    'root' : {
        'level':'INFO',
        'handlers': ['file']
    }
})



SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR,"pybo.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x08a\t\x14\x17\x04\xf1\x90\xaf\xb7@\xdfGizw'