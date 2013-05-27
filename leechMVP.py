__author__ = 'SolPie'
import os
from datetime import datetime

from bottle import (Bottle, request, static_file, TEMPLATE_PATH, jinja2_template as render_template)

from settings import *


app = Bottle()
TEMPLATE_PATH.insert(0, TEMPLATES_PATH)

from utils.dbm import PhotoDBM, TrashDBM
from utils.photos import walkPhotos, walkTrash, Photo
from utils.md5 import md5_bytes, md5_path
## slash test
# from utils.bottleEx import StripPathMiddleware
#
# app = app()
# appEx = StripPathMiddleware(app=app)
##

##dbm test
db = PhotoDBM()
db.open(DB_PATH)
# p = db.get('test')
# p.filename = 'file.jpg'
# p.md5num = 'fe334edf'
# p.path = 23
# p.title = 'hello world'
# db.set('test', p)
# db.sync()
# print db.get('test')
# db.set('test', d)
# db.sync()
##
trash_db = TrashDBM(DBM_TRASH)
# trash_db.set('trash', 'testing')
# print trash_db.get('trash')
##


@app.route('/')
def index():
    h = request.get_header('Referer')
    return render_template('templates/index')


@app.route('/walk')
def walk():
    db.clear()
    p = walkPhotos(PhotoDBM(), PHOTOS_PATH)
    return render_template('walk', photos=p.values())


@app.route('/gallery')
def gallery():
    photos = PhotoDBM().values()
    return render_template('templates/gallery', photos=photos)


@app.route('/trash')
def trash():
    t = walkTrash(trash_db, TRASH_PATH)
    return render_template('trash', trash=t)


from utils.backup import zip_db_photos, zip_path


@app.route('/dl/<backup>')
def download(backup):
    if backup == 'db':
        filename = zip_db_photos(UPLOAD_FOLDER, DB_PATH, 'dl/backup.zip')
        return static_file(filename=filename, root='.', download=True)
    if backup == 'all':
        filename = zip_path('.', 'dl/backup2.zip')
        return static_file(filename=filename, root='.', download=True)
        # return static_file('shelve.db', root='db', download=True)
    return ''


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

    p = Photo(md5num, img.filename)
    db.set(md5num, p)
    db.sync()
    return ''


# @app.route('/reg/<name:re:.*\.(png|jpg)>')
photo_regex = '.*\.(%s)' % '|'.join(ALLOWED_EXTENSIONS)


@app.route('/reg/<name:re:%s>' % photo_regex)
def reg(name):
    return name


# @app.route('/img/<filename:re:[a-z]+.jpg>')
# @app.route('/img/<filename:re:.*\.png>#')
@app.route('/p/<filename:re:%s>' % photo_regex)
def redirectImage(filename):
    #todo decode time from blog
    # img = filename
    return static_file(filename, root=PHOTOS_PATH, mimetype='image/png')
    # return static_file('solpie.png', IMAGE_PATH)
    # return redirect('http://img.solpie.net/?di=ZTZR')


@app.route('/del/p/<filename>')
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


@app.get('/<filename:re:.*\.js>')
def static_js(filename):
    return static_file(filename, root=STATIC_PATH + 'js')


@app.get('/<filename:re:.*\.css>')
def static_css(filename):
    #todo allow referer
    h = request.get_header('Referer')
    return static_file(filename, root=STATIC_PATH + 'css')


@app.get('/img/<filename:re:.*\.(png|jpg)>')
def static_css(filename):
    return static_file(filename, root=STATIC_PATH + 'img')


@app.error(404)
def error404(e):
    return 'Nothing here,sorry:\n' + e.body

# @app.error(500)
# def error500():
#     return '500'


if __name__ == '__main__':
    # run(app=appEx, debug=True, reloader=True)
    app.run(debug=True, reloader=True)