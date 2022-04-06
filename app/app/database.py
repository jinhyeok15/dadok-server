from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime

# dev db RDS 설정
db: str
dbusername: str
dbpassword: str
dbhost: str
dbport: str
dbname: str

SQLALCHEMY_DATABASE_URL = f'{db}://{dbusername}:{dbpassword}@{dbhost}:{dbport}/{dbname}?charset=utf8mb4'

engine = create_engine(SQLALCHEMY_DATABASE_URL, convert_unicode=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

create_now = datetime.utcnow()
modified_now = datetime.utcnow()
