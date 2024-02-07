import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "postgresql://postgres:Pokemon492#@localhost/Product" #for testing local
DATABASE_URL = "postgresql+psycopg2://yoke492:Pokemon492#@/Product?host=/cloudsql/total-method-413610:asia-south2:ondc-hackathon"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# testing conneciton
# engine = sqlalchemy.create_engine(DATABASE_URL)


# try:
#     connection = engine.connect()
#     print("Connection to the database successful!")
#     connection.close()
# except Exception as e:
#     print(f"Error connecting to the database: {e}")
