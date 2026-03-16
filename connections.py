from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

path = "postgresql+psycopg2://app_database_kosh_user:lzELMxoJZwJaHJWwAM3KphuXG6DuBIru@dpg-d6rv1nfafjfc73elqqeg-a.oregon-postgres.render.com:5432/app_database_kosh"

engine = create_engine(path)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()