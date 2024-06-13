from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL

url_object = URL.create(
    "postgresql+pg8000",
    username="db_user",
    password="p@ssw0rd",
    host="codx-minerva.postgres.database.azure.com",
    database="dap_session"
)
# PGHOST = 'codx-minerva.postgres.database.azure.com'
# PGUSER = 'db_user'
# PGPORT = 5432
# database = 'dap_session'
# password = 'p%%40ssw0rd'

# SQLALCHEMY_DATABASE_URL = f"postgresql://{PGUSER}:{password}@{PGHOST}:{PGPORT}/{database}"

engine = create_engine(url_object)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()