__author__ = 'SolPie'
from bottle import Bottle, request, json_loads, static_file, jinja2_template as template

app = Bottle()
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


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
    f = img.file.file.read()
    f2 = open(UPLOAD_FOLDER + img.filename, 'wb')
    f2.write(f)
    f2.close()
    return ''


if __name__ == '__main__':
    app.run(debug=True, reloader=True)