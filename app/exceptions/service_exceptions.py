
class ServiceException(Exception):
    """
    Raised when a service operation fails.
    """
    def __init__(self, message: str = "An unexpected error occurred. Please contact the support team."):
        self.message = message
        super().__init__(self.message)