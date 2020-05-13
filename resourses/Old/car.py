from sqlalchemy import Column, Integer, String
from libs.database import Base, init_db, db_session

class Cars(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    head = Column(String(1024), nullable=False)
    link = Column(String(1024), nullable=False)
    photo = Column(String(1024), nullable=False)
    price = Column(String(1024), nullable=False)


    def __init__(self, head=None, link=None, photo=None, price=None):
        self.head = head.strip()
        self.link = link.strip()
        self.photo = photo.strip()
        self.price = price

    def __repr__(self):
        return '<Cars %r>' % (self.head)

def delete_Users():
    try:
        num_rows_deleted = db_session.query(Cars).delete()
        db_session.commit()
    except:
        db_session.rollback()
#delete_Users()
init_db()






# from flask import Flask, session, g
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
#
#
# # parce = Flask(__name__)
# #
# # POSTGRES = {
# #     'user': 'postgres',
# #     'pw': '123',
# #     'db': 'auto',
# #     'host': 'localhost',
# #     'port': '5432'
# # }
# # # POSTGRES = {
# # #     'user': 'myuser',
# # #     'pw': '123',
# # #     'db': 'postgres',
# # #     'host': 'localhost',
# # #     'port': '5432',
# # # }
# # # 'db': 'site_flask', 'user': 'postgres',
# # parce.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES
# # db = SQLAlchemy(parce)
# # db = Run.db

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
# db.create_all()
# db.session.close()
# def add_cars(self):
#     db.session.add(self.head, self.link, self.photo, self.price)
#     db.session.commit()
#     db.session.close()


# db.session.add(Cars(n, l, f, p))

