__author__ = 'SolPie'
import os
from datetime import datetime

from bottle import (Bottle, request, static_file,
                    TEMPLATE_PATH, jinja2_template as render_template)

from settings import *


app = Bottle()
TEMPLATE_PATH.insert(0, TEMPLATES_PATH)
##dbm
from utils.dbm import DBM
from utils.photos import walkImages, walkTrash
from utils.md5 import md5_bytes, md5_path

db = DBM()
db.open(DB_PATH)
p = db.get('test')
# p.filename = 'file.jpg'
# p.md5num = 'fe334edf'
# p.path = 23
# p.title = 'hello world'
# db.set('test', p)
db.sync()
print db.get('test')
# db.set('test', d)
# db.sync()
##
@app.route('/')
def index():
    return render_template('templates/index')


@app.route('/walk')
def walk():
    walkImages(DBM(), PHOTOS_PATH)


@app.route('/gallery')
def gallery():
    photos = DBM().get('photos')
    return render_template('templates/gallery', photos=photos)


@app.route('/trash')
def trash():
    t = walkTrash(db, TRASH_PATH)
    return render_template('trash', trash=t)


@app.route('/upload', method='POST')
def upload():
    img = request.files['uploaded_file']
    chuck = img.file.read()
    # #todo check if name is same
    # #todo security filename
    f2 = open(PHOTOS_PATH + img.filename, 'wb')
    f2.write(chuck)
    f2.close()
    md5num = md5_bytes(chuck)
    db.set(md5num, img.filename)
    db.sync()
    return ''


@app.route('/reg/<name:re:[a-z]+.jpg>')
def reg(name):
    return name


# @app.route('/img/<filename:re:[a-z]+.jpg>')
# @app.route('/img/<filename:re:.*\.png>#')
@app.route('/img/<filename>')
def redirectImage(filename):
    # img = filename
    return static_file(filename, root=PHOTOS_PATH, mimetype='image/png')
    # return static_file('solpie.png', IMAGE_PATH)
    # return redirect('http://img.solpie.net/?di=ZTZR')


@app.route('/del/img/<filename>')
def delete_file(filename):
    old = PHOTOS_PATH + filename
    now = datetime.now().strftime('%Y%b%a%H%M%S')
    new = TRASH_PATH + now + '_' + filename
    db.del_key(md5_path(old))
    db.sync()
    if os.path.isfile(old):
        os.rename(old, new)
        log = 'delete photos', filename
        return log
    else:
        log = 'photos is not exists'
        return log


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


@app.error(404)
def error404():
    return 'Nothing here,sorry'

# @app.error(500)
# def error500():
#     return '500'


if __name__ == '__main__':
    app.run(debug=True, reloader=True)