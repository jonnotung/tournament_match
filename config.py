import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
		SECRET_KEY = os.environ.get('SECRET_KEY') or '132f93f574e7b1fcd5cd2c70555f0683'
		SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
		SQLALCHEMY_TRACK_MODIFICATIONS = False