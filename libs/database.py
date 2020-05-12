from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


POSTGRES = {
    'user': 'postgres',
    'pw': '123',
    'db': 'auto',
    'host': 'localhost',
    'port': '5432',
}

engine = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES, convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import libs.car
    # import libs.users
    # import libs.message
    Base.metadata.create_all(bind=engine)

# def create():
# engine = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES, convert_unicode=True)
# metadata = MetaData()
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=engine))
#

#
# def init_db():
#     metadata.create_all(bind=engine)
