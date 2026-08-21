from app.schemas.customer_schema import CustomerRegistrationSchema
from app.services import CustomerService
from app.database import db   
from fastapi import APIRouter, status
from loguru import logger

api_router = APIRouter()

# Dependency injection
customer_service = CustomerService(db_manager=db)    

@api_router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"message": "Hello from smoothie-registration!"}

@api_router.post('/customers/register', status_code=201)
def register_customer(validated_body: CustomerRegistrationSchema):
    
    logger.info(f"Received registration request for customer with email: {validated_body.email}")
    
    response = customer_service.register_customer(validated_body.model_dump())
    logger.info(f"Customer registered successfully with ID: {response['customer_id']}")

    return {
        "status": "success",
        "message": "Customer registered for smoothies successfully",
        "data": response
    }