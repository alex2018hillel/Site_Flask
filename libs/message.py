from sqlalchemy import Column, Integer, String
from libs.database import Base, init_db, db_session

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


def delete_Message():
    try:
        num_rows_deleted = db_session.query(Message).delete()
        db_session.commit()
    except:
        db_session.rollback()

init_db()
