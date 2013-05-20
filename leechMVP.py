__author__ = 'SolPie'
from bottle import Bottle, request, redirect, json_loads, static_file, jinja2_template as template

app = Bottle()
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
IMAGE_PATH = 'uploads/images/'


@app.route('/')
def index():
    return template('templates/index')


@app.get('/<filename:path>')
def static_files(filename):
    print filename
    return static_file(filename, '.')


@app.route('/upload', method='POST')
def upload():
    img = request.files['uploaded_file']
    f = img.file.read()
    #todo check if name is same
    #todo security filename
    f2 = open(IMAGE_PATH + img.filename, 'wb')
    f2.write(f)
    f2.close()
    return ''


@app.route('/img')
def redirectImage():
    return static_file('solpie.png', IMAGE_PATH)
    # return redirect('http://img.solpie.net/?di=ZTZR')


if __name__ == '__main__':
    app.run(debug=True, reloader=True)