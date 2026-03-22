import pytest
from app.models import CustomerRequest, Ticket, ContractType
from app.rules import evaluate_churn_risk

def make_tickets(n, days_ago=5, category="technical"):
    return [Ticket(ticket_id=f"T{i}", days_ago=days_ago, category=category) for i in range(n)]

# Rule 1 tests
def test_high_risk_more_than_5_tickets():
    customer = CustomerRequest(
        customer_id="C001",
        contract_type=ContractType.month_to_month,
        monthly_charge=70.0,
        tickets=make_tickets(6, days_ago=10),
    )
    result = evaluate_churn_risk(customer)
    assert result.risk_level == "HIGH"
    assert result.tickets_last_30_days == 6

def test_not_high_if_tickets_outside_30_days():
    customer = CustomerRequest(
        customer_id="C002",
        contract_type=ContractType.month_to_month,
        monthly_charge=70.0,
        tickets=make_tickets(6, days_ago=40),   # outside 30-day window
    )
    result = evaluate_churn_risk(customer)
    assert result.risk_level != "HIGH"

# Rule 2 tests
def test_high_risk_month_to_month_with_complaint():
    customer = CustomerRequest(
        customer_id="C003",
        contract_type=ContractType.month_to_month,
        monthly_charge=55.0,
        tickets=[Ticket(ticket_id="T1", days_ago=5, category="complaint")],
    )
    result = evaluate_churn_risk(customer)
    assert result.risk_level == "HIGH"
    assert result.has_complaint is True

def test_no_high_risk_two_year_with_complaint():
    customer = CustomerRequest(
        customer_id="C004",
        contract_type=ContractType.two_year,
        monthly_charge=55.0,
        tickets=[Ticket(ticket_id="T1", days_ago=5, category="complaint")],
    )
    result = evaluate_churn_risk(customer)
    assert result.risk_level != "HIGH"

# Rule 3 tests
def test_medium_risk_3_tickets():
    customer = CustomerRequest(
        customer_id="C005",
        contract_type=ContractType.one_year,
        monthly_charge=60.0,
        tickets=make_tickets(3, days_ago=10),
    )
    result = evaluate_churn_risk(customer)
    assert result.risk_level == "MEDIUM"

# Default LOW tests
def test_low_risk_no_tickets():
    customer = CustomerRequest(
        customer_id="C006",
        contract_type=ContractType.two_year,
        monthly_charge=80.0,
        tickets=[],
    )
    result = evaluate_churn_risk(customer)
    assert result.risk_level == "LOW"

def test_low_risk_2_tickets():
    customer = CustomerRequest(
        customer_id="C007",
        contract_type=ContractType.one_year,
        monthly_charge=80.0,
        tickets=make_tickets(2, days_ago=10),
    )
    result = evaluate_churn_risk(customer)
    assert result.risk_level == "LOW"