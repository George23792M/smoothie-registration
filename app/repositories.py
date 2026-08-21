
from loguru import logger
from app.models import Customer, CustomerPreference, Subscription, WorkflowRun


class CustomerRepository:
    def save_customer(self, session, data: dict) -> dict:
        
        customer = Customer(
            first_name = data.get("first_name"),
            middle_name = data.get("middle_name"),
            last_name = data.get("last_name"),
            preferred_name = data.get("preferred_name"),
            email = data.get("email"),
        )
        session.add(customer)
        session.flush()  # Flush to get the generate customer Id
        
        subscription = Subscription(
            customer_id = customer.id,
            plan_name = data.get("plan_name", "Basic - Standard Smoothie Plan"),
            start_date = data.get("start_date"),
            end_date = data.get("end_date"))
        session.add(subscription)
        session.flush()  # Flush to get the generated subscription Id
        
        prefes_data = data.get("preferences", {})
        preferences = CustomerPreference(
            customer_id = customer.id,
            profile_name = prefes_data.get("profile_name", "Default Profile"),
            days = prefes_data.get("days", 7),
            max_calories = prefes_data.get("max_calories", 500),
            nut_free = prefes_data.get("nut_free", False),
            gluten_free = prefes_data.get("gluten_free", False),
            dairy_free = prefes_data.get("dairy_free", False),
            soy_free = prefes_data.get("soy_free", False)
        )
        session.add(preferences)
        session.flush()  # Flush to get the generated preference Id
        
        workflow_run = WorkflowRun(
            customer_id = customer.id,
            status = "PENDING",
            attempt_count = 0,
            validation_errors = None,
            email_status = "PENDING",
            workflow_type = "NEW_REGISTRATION"
        )
        session.add(workflow_run)
        session.flush()  # Flush to get the generated workflow run Id
        
        logger.info(f"Customer {customer.id} saved successfully with subscription {subscription.id}, preferences {preferences.id}, and workflow run {workflow_run.id}.")
        
        return{
            "customer_id": str(customer.id),
            "subscription_id": str(subscription.id),
            "subscription_status": subscription.status,
            "preference_id": str(preferences.id)
        }
            