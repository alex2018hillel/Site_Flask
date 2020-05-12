from sqlalchemy import Column, Integer, String
from libs.database import Base

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    text = Column(String(1024), nullable=False)
    data1 = Column(String(1024), nullable=False)


    def __init__(self, text=None, data1=None):
        self.text = text.strip()
        self.data1 = data1.strip()


    def __repr__(self):
        return '<Message %r>' % (self.text)

# class Tag(Base):
#     __tablename__ = 'tag'
#     id = Column(Integer, primary_key=True)
#     text = Column(String(32), nullable=False)

    # message_id = Column(Integer, ForeignKey('message.id'), nullable=False)
    # message = relationship('Message', backref=backref('tags', lazy=True))




# message = Flask(__name__)
#
# POSTGRES = {
#     'user': 'postgres',
#     'pw': '123',
#     'db': 'auto',
#     'host': 'localhost',
#     'port': '5432'
# }
# message.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES
# #app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:123@localhost:5432/site_flask"
# db = SQLAlchemy(message)
# db = app.db

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(1024), nullable=False)
#     data1 = db.Column(db.String(1024), nullable=False)
#
#     def __init__(self, text, tags, data1, sort="Message.text"):
#         self.text = text.strip()
#         self.data1 = data1.strip()
#         self.tags = [Tag(text=tag.strip()) for tag in tags.split(',')]
#
#
# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(32), nullable=False)
#
#     message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
#     message = db.relationship('Message', backref=db.backref('tags', lazy=True))
#
#
# db.create_all()
# db.session.close()