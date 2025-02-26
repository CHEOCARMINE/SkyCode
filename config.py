# config.py

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def get_db_connection(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ulzjbyhniqbdiwgh:6dJiPKrE1AXfiS1jsfOV@bef4yknw2tlo8ei20zko-mysql.services.clever-cloud.com:3306/bef4yknw2tlo8ei20zko'
    db.init_app(app)
    return db
