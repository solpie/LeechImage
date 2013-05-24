__author__ = 'SolPie'
from bottle import (Bottle, request, static_file, jinja2_template as render_template)

app = Bottle()

# from utils.bottleRedis import RedisPlugin
#
# p = RedisPlugin(host='localhost')
# app.install(p)

from utils.photos import walkImages

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
IMAGE_PATH = 'uploads/images/'

import anydbm


def create_db():
    try:
        db = anydbm.open('db', 'c')
        for k, v in db.iteritems():
            print k, '\t', v
        return db
    finally:
        pass
        # db.close()


# _db = create_db()


@app.route('/')
def index():
    # for root, dirs, files in os.walk('uploads/images/'):
    #     walkImages(create_db(), files)
    # if _db:
    #     pass
    # else:
    #     db = create_db()
    #     walkImages(db, 'uploads/images/')
    db = create_db()
    walkImages(db, 'uploads/images/')
    db.close()
    return render_template('templates/index')


@app.route('/walk')
def walk():
    pass


@app.route('/gallery')
def gallery():
    db = create_db()
    return render_template('templates/gallery', db=db)


@app.route('/upload', method='POST')
def upload():
    img = request.files['uploaded_file']
    chuck = img.file.read()
    # #todo check if name is same
    # #todo security filename
    ##todo save file deco :set md5 ,close db
    f2 = open(IMAGE_PATH + img.filename, 'wb')
    f2.write(chuck)
    f2.close()
    # md5num = md5_bytes(chuck)
    # db[md5num] = img.filename
    ###
    return ''


# @app.route('/img')
@app.route('/img/<filename>')
def redirectImage(filename):
    return static_file(filename, IMAGE_PATH)
    # return static_file('solpie.png', IMAGE_PATH)
    # return redirect('http://img.solpie.net/?di=ZTZR')


@app.route('/redis')
def redis(rdb):
    row = rdb.get('45307f2ed107d41180a9ca446c8fa1d0')
    if row:
        return row
    else:
        return 'hehe...'


@app.get('/<filename:path>')
def static_files(filename):
    print filename
    return static_file(filename, '.')


if __name__ == '__main__':
    app.run(debug=True, reloader=True)