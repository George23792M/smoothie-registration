
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()  # Load environment variables from .env file

# Fetch database level configuration from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Connection details for the database
POOL_SIZE = int(os.getenv("POOL_SIZE", 2))
MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", 5))
POOL_TIMEOUT = int(os.getenv("POOL_TIMEOUT", 15))
POOL_RECYCLE = int(os.getenv("POOL_RECYCLE", 1000))

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    pool_recycle=POOL_RECYCLE,
    pool_pre_ping=True  # Enable pre-ping to check if connections are alive
)

# creating a session used for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_db_connection() -> bool:
    "Check if the database connection is successful."
    try: 
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Database connection successful.")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
    