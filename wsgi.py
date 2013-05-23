__author__ = 'SolPie'
import os
import sys

sys.path.insert(0, os.path.join('.', 'site-packages'))
###
import anydbm

# Open database, creating it if necessary.
db = anydbm.open('cache', 'c')

# Record some values
db['www.python.org'] = 'Python Website'
db['www.cnn.com'] = 'Cable News Network'

# Loop through contents.  Other dictionary methods
# such as .keys(), .values() also work.
for k, v in db.iteritems():
    print k, '\t', v

# Close when done.
db.close()
###
from leechMVP import app

application = app

if __name__ == '__main__':
    app.run(debug=True)