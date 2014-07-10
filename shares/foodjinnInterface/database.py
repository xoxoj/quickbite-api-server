from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

uri = os.environ.get('DATABASE_URL', 'postgres://postgres:postgres@192.168.178.44:5432/foodjinn')
#uri = os.environ.get('DATABASE_URL', 'postgres://postgres:postgres@192.168.33.10:5430/foodjinnGeo')
engine = create_engine(uri, convert_unicode=False)
db_session = scoped_session(sessionmaker(autocommit=False,
					 autoflush=False,
					 bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  import foodjinnInterface.models
  Base.metadata.create_all(bind=engine)
