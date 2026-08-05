

from loguru import logger
from app.database import DatabaseManager
from app.repositories import CustomerRepository


class CustomerService:
    
    """
    Business logic layer. 
    Manages atomic transactions and workflow logic.
    """
    
    def __init__(self,db_manager: DatabaseManager, repository: CustomerRepository = None):
        self.db_manager = db_manager
        self.repository = repository is not None and repository or CustomerRepository()
        
    def register_customer(self, data: dict) -> dict:
        """
        Registers a new customer along with their subscription and preferences.
        This method ensures that all operations are performed within a single transaction.
        
        Args:
            data (dict): A dictionary containing customer, subscription, and preference details.
        
        Returns:
            dict: A dictionary containing the IDs of the created customer, subscription, and preferences.
        """
        with self.db_manager.transaction() as session:
            try:
                result = self.repository.save_customer(session, data)
                logger.info(f"Transaction committed successfully for customer ID {result['customer_id']}.")
                return result
            except Exception as e:
                session.rollback()  # Rollback the transaction in case of an error
                raise e