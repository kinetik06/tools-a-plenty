activate_this = '/var/www/itemcatalogproject/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys

sys.path.append('/home/ubuntu/item-catalog-project/')

from toolcatalog import app as application
