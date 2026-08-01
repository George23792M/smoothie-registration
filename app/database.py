
from contextlib import contextmanager
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()  # Load environment variables from .env file

class DatabaseManager:
    def __init__(self, app=None):
        self.engine = None
        self.SessionLocal = None
        if app:
            self.init_app(app)
            
    def init_app(self, app):
        "Initialize sql engine and session maker with the Flask app context"
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        pool_size = int(os.getenv("DB_POOL_SIZE", 5))  # Default pool size is 5 if not set
        max_overflow = int(os.getenv("DB_MAX_OVERFLOW", 10))  # Default max overflow is 10 if not set
        pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", 30))  # Default pool timeout is 30 seconds if not set
        pool_recycle = int(os.getenv("DB_POOL_RECYCLE", 1800))  # Default pool recycle is 1800 seconds (30 minutes) if not set
        
        self.engine = create_engine(
            database_url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,
            pool_pre_ping=True)  # Enable pool pre-ping to check connections before using them
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    @contextmanager    
    def transaction(self):
        """"
        Context manager for database transactions.
        Usage:
            with db_manager.transaction() as session:
                # Perform database operations using the session
        """
        
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()