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

def delete_Cars():
    try:
        num_rows_deleted = db_session.query(Cars).delete()
        db_session.commit()
    except:
        db_session.rollback()
# delete_Cars()
init_db()

