import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from blog import app


basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'blog.db'), convert_unicode=True)
db = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                 bind=engine))

Base = declarative_base()
Base.query = db.query_property()

@app.teardown_request
def shutdown_session(exception=None):
    db.remove()

def init_db():
    from blog import models
    Base.metadata.create_all(bind=engine)