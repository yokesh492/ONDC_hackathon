import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from google.cloud.sql.connector import Connector, IPTypes


def get_gcloud_connection() -> sqlalchemy.engine.base.Engine:
    connector = Connector()

    def connect() -> None:
        return connector.connect(
            os.environ["INSTANCE_CONNECTION_NAME"],
            "pg8000",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            db=os.environ["DB_NAME"],
            ip_type=IPTypes.PUBLIC,
        )

    # Create the SQLAlchemy engine using the connector
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=connect,
    )
    return engine


def get_vps_connection() -> sqlalchemy.engine.base.Engine:
    DB_USER = os.getenv("DB_USER", "yoke492")
    DB_PASS = os.getenv("DB_PASS", "Pokemon492#")
    DB_NAME = os.getenv("DB_NAME", "ONDC")
    DB_HOST = os.getenv("DB_HOST", "91.108.104.64")
    DB_PORT = os.getenv("DB_PORT", "5432")

    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Create the connection pool using SQLAlchemy
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    return engine


def get_engine() -> sqlalchemy.engine.base.Engine:
    environment = os.environ.get("ENVIRONMENT", "development")
    if environment == "production_gcloud":
        return get_gcloud_connection()
    elif environment == "production_vps":
        return get_vps_connection()
    else:
        # Default local database connection for development
        SQLALCHEMY_DATABASE_URL = "postgresql://yoke492:Pokemon492#@91.108.104.64:5432/ondc"
        return create_engine(SQLALCHEMY_DATABASE_URL)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()