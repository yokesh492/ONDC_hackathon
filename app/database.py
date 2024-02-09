import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os


def connect_cloud_sql() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of Postgres."""
    db_user = os.environ["DB_USER"]  # e.g. 'my-database-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-database-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
    db_host = os.environ["DB_HOST"]  # Public IP of the Cloud SQL instance

    # Create the connection pool using SQLAlchemy
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+psycopg2",  # Using psycopg2 as the database adapter
            username=db_user,
            password=db_pass,
            host=db_host,  # Use the public IP address here
            port=5432,  # Default port for PostgreSQL
            database=db_name,
        ),
        # Other engine configurations as needed
    )
    return pool

# Create the engine
#engine = connect_cloud_sql()





# #DATABASE_URL = "postgresql://postgres:Pokemon492#@localhost/Product" #for testing local
# #DATABASE_URL = "postgresql+psycopg2://yoke492:Pokemon492#@/Product?host=/cloudsql/total-method-413610:asia-south2:ondc-hackathon"
# def connect_cloud_sql() -> sqlalchemy.engine.base.Engine:
#     """Initializes a Unix socket connection pool for a Cloud SQL instance of Postgres."""
#     # Note: Saving credentials in environment variables is convenient, but not
#     # secure - consider a more secure solution such as
#     # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
#     # keep secrets safe.
#     db_user = os.environ["DB_USER"]  # e.g. 'my-database-user'
#     db_pass = os.environ["DB_PASS"]  # e.g. 'my-database-password'
#     db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
#     instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]  # e.g. 'project:region:instance'

#     # Construct the Unix socket path
#     unix_socket_path = f"/cloudsql/{instance_connection_name}"

#     # Create the connection pool using SQLAlchemy
#     pool = sqlalchemy.create_engine(
#         sqlalchemy.engine.url.URL.create(
#             drivername="postgresql+pg8000",
#             username=db_user,
#             password=db_pass,
#             database=db_name,
#             query={"unix_sock": f"{unix_socket_path}/.s.PGSQL.5432"},
#         ),
#         # Other engine configurations as needed
#     )
#     return pool

# # Create the engine and metadata
# engine = connect_cloud_sql()


#connecting railywway postgres 
DATABASE_URL = os.getenv("DB_URL") 
engine = create_engine(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# # Bind the sessionmaker to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# testing conneciton
# engine = sqlalchemy.create_engine(DATABASE_URL)


# try:
#     connection = engine.connect()
#     print("Connection to the database successful!")
#     connection.close()
# except Exception as e:
#     print(f"Error connecting to the database: {e}")
