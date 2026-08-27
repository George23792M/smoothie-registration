from app.exceptions.service_exceptions import ServiceException


class CustomerAlreadyExistsException(ServiceException):
    """
    Raised when a customer already exists
    """
    def __init__(self, message: str = "Customer Already exists with this email address"):
        self.message = message
        super().__init__(self.message)