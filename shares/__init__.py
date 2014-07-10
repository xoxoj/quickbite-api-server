from __future__ import with_statement
from contextlib import closing
from FoodjinnInterface.database import db_session
from flask import Flask

#configuration
# DATABASE = '/tmp/FoodjinnInterface.db'
# DEBUG = True
# SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

import foodjinnInterface.views

@app.teardown_request
def teardown_request(exception):
  db_session.remove()

