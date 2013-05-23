__author__ = 'SolPie'
from bottle import (Bottle, request, static_file, jinja2_template as render_template)

app = Bottle()

from utils.bottleRedis import RedisPlugin

p = RedisPlugin(host='localhost')
app.install(p)

from hashlib import md5
import tempfile
import os
from utils.photos import walkImages

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
IMAGE_PATH = 'uploads/images/'


def create_db():
    import anydbm

    db = anydbm.open('db', 'c')
    for k, v in db.iteritems():
        print k, '\t', v
    return db


@app.route('/')
def index():
    # for root, dirs, files in os.walk('uploads/images/'):
    #     walkImages(create_db(), files)
    walkImages(create_db(), 'uploads/images/')
    return render_template('templates/index')


@app.route('/gallery')
def gallery():
    db = create_db()
    return render_template('templates/gallery', db=db)


@app.route('/upload', method='POST')
def upload(rdb):
    img = request.files['uploaded_file']
    chuck = img.file.read()
    # #todo check if name is same
    # #todo security filename
    # f2 = open(IMAGE_PATH + img.filename, 'wb')
    # f2.write(chuck)
    # f2.close()
    ###
    tmp = tempfile.mkstemp()
    md5_ = md5()
    orig = file.name
    f = os.fdopen(tmp[0], 'wb+')
    # for chuck in file.chucks():
    f.write(chuck)
    md5_.update(chuck)
    f.close()
    md5sum = md5_.hexdigest()#'45307f2ed107d41180a9ca446c8fa1d0'
    rdb.set(md5sum, IMAGE_PATH + img.filename)
    return md5sum


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