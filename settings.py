__author__ = 'SolPie'

DB_ENGINE = 'shelve'
DB_PATH = 'db/shelve.db'
DBM_TRASH = 'db/trash.dbm'

TEMPLATES_PATH = 'templates'
STATIC_PATH = 'static/'

ALLOWED_REFERER = ['http://localhost:8080', 'http://www.solpie.net', '^http://(.)+\.solpie\.net']

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
MUSIC_PATH = 'uploads/images/'
VIDEO_PATH = 'uploads/images/'
PHOTOS_PATH = 'uploads/images/'
TRASH_PATH = 'uploads/trash/'

ADMIN = ('admin', '-+')