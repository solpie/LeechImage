__author__ = 'SolPie'
from bottle import (Bottle, request, static_file, jinja2_template as render_template)

app = Bottle()

# from utils.bottleRedis import RedisPlugin
#
# p = RedisPlugin(host='localhost')
# app.install(p)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
IMAGE_PATH = 'uploads/images/'

##dbm


from utils.dbm import DBM
from utils.photos import walkImages
db = DBM()
db.open('shelve')
# d = {}
# d['sf'] = 5
# db.set('test', d)
# db.sync()
##

@app.route('/')
def index():
    db = DBM()
    print '.....', db.get('test')
    return render_template('templates/index')


@app.route('/walk')
def walk():
    walkImages(DBM(),IMAGE_PATH)
    pass


@app.route('/gallery')
def gallery():
    return render_template('templates/gallery', db=DBM())


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