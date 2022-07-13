import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:awa@localhost/jesus'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DEBUG = True

# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = '<Put your local database url>'
