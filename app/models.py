from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ContractType(str, Enum):
    month_to_month = "Month-to-Month"
    one_year = "One Year"
    two_year = "Two Year"

class Ticket(BaseModel):
    ticket_id: str
    days_ago: int          # how many days ago the ticket was raised
    category: str          # e.g. "complaint", "billing", "technical"

class CustomerRequest(BaseModel):
    customer_id: str
    contract_type: ContractType
    monthly_charge: float
    previous_monthly_charge: Optional[float] = None
    tickets: List[Ticket] = []

class RiskResponse(BaseModel):
    customer_id: str
    risk_level: str        # LOW, MEDIUM, HIGH
    reasons: List[str]
    tickets_last_30_days: int
    has_complaint: bool