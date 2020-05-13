from sqlalchemy import Column, Integer, String
from libs.database import Base, init_db, db_session

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(1024), nullable=False)
    password = Column(String(1024), nullable=False)


    def __init__(self, login=None, password=None):
        self.login = login.strip()
        self.password = password.strip()


    def __repr__(self):
        return '<Users %r>' % (self.login)

    def get_users():
        users = []
        for class_instance in db_session.query(Users).all():
            u = vars(class_instance)
            users.append(u.get('login'))
            #users.append(u.get('password'))
        return users

def get_password(login):
    pas = db_session.query(Users).filter_by(login=login).one()
    print(pas.password)
    return pas.password


def delete_Users():
    try:
        num_rows_deleted = db_session.query(Users).delete()
        db_session.commit()
    except:
        db_session.rollback()



# delete_Users()
init_db()


'''
ubuntu
sudo apt-get update -y
sudo apt-get install -y python-flask-httpauth
'''