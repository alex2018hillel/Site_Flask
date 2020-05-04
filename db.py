import requests
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2 import sql
from contextlib import closing
from sqlalchemy import MetaData, create_engine, Table

parce = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': '123',
    'db': 'site_flask',
    'host': 'localhost',
    'port': '5432',
}
parce.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES
db = SQLAlchemy(parce)

class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(1024), nullable=False)
    password = db.Column(db.String(1024), nullable=False)


    def __init__(self, name, password):
        self.login = name.strip()
        self.password = password.strip()

deleted_objects = Users.__table__.delete()
engine = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES, echo=False)

engine.execute(deleted_objects)

db.create_all()

def post_db(login, password):
    db.session.add(Users(login, password))
    db.session.commit()

post_db('darya', 'tropp')
post_db('kira', 'tropp1')


def get_password(username):
    user = Users.query.filter_by(login=username).first()
    return user.password

def get_id(username):
    user = Users.query.filter_by(login=username).first()
    return user.id

print(get_password('kira'))
print(get_id('kira'))


# from yourapp import User    ?????????????????????????????????
me = Users('admin', 'admin@example.com')
db.session.add(me)
db.session.commit()
print(me.id)
db.session.delete(me)
db.session.commit()

#==============================================================
# def get_db():
#     """Connect to the application's configured database. The connection
#     is unique for each request and will be reused if this is called
#     again.
#     """
#     if "db" not in g:
#         g.db = sqlite3.connect(
#             current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
#
#     return g.db
#=============================================================

# class Cars(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     head = db.Column(db.String(1024), nullable=False)
#     link = db.Column(db.String(1024), nullable=False)
#     photo = db.Column(db.String(1024), nullable=False)
#     price = db.Column(db.String(1024), nullable=False)
#
#     def __init__(self, head, link, photo, price):
#         self.head = head.strip()
#         self.link = link.strip()
#         self.photo = photo.strip()
#         self.price = price.strip()
#
# deleted_objects = Cars.__table__.delete()
# engine = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES, echo=False)
#
# engine.execute(deleted_objects)
#
# db.create_all()

# def get_db():
#     """Connect to the application's configured database. The connection
#     is unique for each request and will be reused if this is called
#     again.
#     """
#     if "db" not in g:
#         g.db = sqlite3.connect(
#             current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
#
#     return g.db
#
# def close_db(e=None):
#     """If this request connected to the database, close the
#     connection.
#     """
#     db = g.pop("db", None)
#
#     if db is not None:
#         db.close()
#
#
# def init_db():
#     """Clear existing data and create new tables."""
#     db = get_db()
#
#     with current_app.open_resource("schema.sql") as f:
#         db.executescript(f.read().decode("utf8"))