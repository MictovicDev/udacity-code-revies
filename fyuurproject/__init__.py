import collections
import json
import os
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from fyuurproject.config import Config



app = Flask(__name__)
collections.Callable = collections.abc.Callable
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db) 

app.config.from_object(Config)


from fyuurproject import routes
 

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')