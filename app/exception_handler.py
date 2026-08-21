from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.exceptions.service_exceptions import ServiceException
from app.schemas import ErrorDetail, ErrorResponseSchema

def register_exception_handlers(app):
    """
    Registers custom exception handlers for the FastAPI application.
    """
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, e: RequestValidationError):

        # Transform Pydantic's raw error dicts into your custom ErrorDetail model
        formatted_errors = [
            ErrorDetail(
                location=list(error['loc']),
                message=error['msg'],
                type=error['type']
            )
            for error in e.errors()
        ]
        
        error_response = ErrorResponseSchema(
            message="Validation failed",
            errors=formatted_errors
        )
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )
        
    @app.exception_handler(ServiceException)
    async def service_exception_handler(request: Request, e: ServiceException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": e.message
            }
        )    