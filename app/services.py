
from app.exceptions.db_exceptions import TransientDatabaseException
from app.exceptions.service_exceptions import ServiceException
from app.exceptions.custom_exceptions import CustomerAlreadyExistsException

from loguru import logger
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from tenacity import stop
from app.database import DatabaseManager
from app.repositories import CustomerRepository
from app.config.config import settings


class CustomerService:
    
    """
    Business logic layer. 
    Manages atomic transactions and workflow logic.
    """
    
    def __init__(self,db_manager: DatabaseManager, repository: CustomerRepository = None):
        self.db_manager = db_manager
        self.repository = repository is not None and repository or CustomerRepository()
        
     
    @retry(
        stop=stop_after_attempt(settings.DB_RETRY_ATTEMPTS),
        wait=wait_exponential(
            min=settings.DB_RETRY_MIN_WAIT,
            max=settings.DB_RETRY_MAX_WAIT,
            multiplier=settings.DB_RETRY_MULTIPLIER        
            ),
        #onLY RETRY ON: 
        retry=retry_if_exception_type((TransientDatabaseException)),
        reraise=True
        )
    def register_customer(self, data: dict) -> dict:
        """
        Registers a new customer along with their subscription and preferences.
        This method ensures that all operations are performed within a single transaction.
        
        Flow: 
        1. Validates that email doesn't already exist (raises CustomerAlreadyExistsException)
        2. If valid, save the customer details with subscription, preferences, and workflow run
        3. All operations within a single atomic transcation
        
        Args:
            data (dict): A dictionary containing customer, subscription, and preference details.
        
        Returns:
            dict: A dictionary containing the IDs of the created customer, subscription, and preferences.
        """
        with self.db_manager.transaction() as session:
            try:
                
                #step 1
                email_address = data.get("email")
                result = self.repository.check_customer_exists_by_email(session,email_address)
                
                #step 2
                if (result):
                    logger.warning(f"Duplicate registration attempt for customer")
                    raise CustomerAlreadyExistsException()
                    
                #step 3
                result = self.repository.save_customer(session, data)
                logger.info(f"Transaction committed successfully for customer ID {result['customer_id']}.")
                return result
            except Exception as e:
                session.rollback()
                
                if isinstance(e, CustomerAlreadyExistsException):
                    raise
                
                #Do not rety business/constraint violoation error
                if "duplicate key" in str(e).lower() or "integrity error" in str(e).lower():
                    logger.error("Integrity constraint violation error. Aborting retries")
                    
                # Retry only on transient database errors
                error_name = type(e).__name__.lower()
                if any(err in error_name for err in ["operational", "interface", "timeout"]):
                    logger.warning(f"Transient database error detected: {e}. Raising custom retryable error. ")
                    raise TransientDatabaseException(str(e).lower()) from e
                
                #for other type errors. Failed immediately.
                logger.error(f"Unexpected error occured during registration process: {e}")
                raise ServiceException()