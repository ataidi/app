from connections import Base, engine
from models import Products

Base.metadata.create_all(bind=engine)