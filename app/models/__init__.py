from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.customer import Customer
from app.models.subscription import Subscription
from app.models.preference import CustomerPreference