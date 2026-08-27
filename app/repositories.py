
from loguru import logger
from app.models import Customer, CustomerPreference, Subscription, WorkflowRun
from sqlalchemy import select, exists


class CustomerRepository:
    
    def save_customer(self, session, data: dict) -> dict:
        
        prefs = self._extract_customer_preferences(data.get("preferences", {}))
        
        subscription = Subscription(
            plan_name = data.get("plan_name", "Basic - Standard Smoothie Plan"),
            start_date = data.get("start_date"),
            end_date = data.get("end_date"))
        
        preferences = CustomerPreference(**prefs)
        
        workflow_run = WorkflowRun(
            status = "PENDING",
            attempt_count = 0,
            validation_errors = None,
            email_status = "PENDING",
            workflow_type = "NEW_REGISTRATION"
        )
        
        customer = Customer(
                    first_name = data.get("first_name"),
                    middle_name = data.get("middle_name"),
                    last_name = data.get("last_name"),
                    preferred_name = data.get("preferred_name"),
                    email = data.get("email"),
                    subscriptions=[subscription],
                    preferences=[preferences],
                    workflow_runs=[workflow_run],
                )
        
        session.add(customer)
        session.flush()

        
        logger.info(f"Customer {customer.id} registered successfully")
        
        return{
            "customer_id": str(customer.id),
            "subscription_id": str(subscription.id),
            "subscription_status": subscription.status,
            "preference_id": str(preferences.id)
        }
        
    def check_customer_exists_by_email(self, session, email: str) -> bool:    
        stmt = select(exists().where(Customer.email == email))
        return session.scalar(stmt)
    
    @staticmethod
    def _extract_customer_preferences(pref_dict: dict) -> dict:    
        return {
            "profile_name": pref_dict.get("profile_name", "Default Profile"),
            "days": max(1, min(30, pref_dict.get("days", 7))),
            "max_calories": max(100, pref_dict.get("max_calories", 500)),
            "nut_free": bool(pref_dict.get("nut_free", False)),
            "gluten_free": bool(pref_dict.get("gluten_free", False)),
            "dairy_free": bool(pref_dict.get("dairy_free", False)),
            "soy_free": bool(pref_dict.get("soy_free", False)),
        }
            