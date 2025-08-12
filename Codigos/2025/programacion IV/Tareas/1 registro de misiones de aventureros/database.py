from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///1 registro de misiones de aventureros", echo = false)
Session = sessionmaker(bind = engine)
Session = Session()

