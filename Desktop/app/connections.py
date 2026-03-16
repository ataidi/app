from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection URL from Render
path = "postgresql+psycopg2://app_database_kosh_user:lzELMxoJZwJaHJWwAM3KphuXG6DuBIru@dpg-d6rv1nfafjfc73elqqeg-a.oregon-postgres.render.com:5432/app_database_koshv"

# Create SQLAlchemy engine
engine = create_engine(path)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Base class for declarative models
Base = declarative_base()