__author__ = 'SolPie'
import os
import sys

sys.path.insert(0, os.path.join('.', 'site-packages'))
###
###
from leechMVP import app

application = app

if __name__ == '__main__':
    app.run(debug=True)