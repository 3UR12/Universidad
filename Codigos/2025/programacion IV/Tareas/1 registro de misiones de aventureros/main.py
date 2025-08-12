from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///orden_magica.db", echo = false)
Session = sessionmaker(bind = engine)
Session = Session()
