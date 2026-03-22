from app.models import CustomerRequest, RiskResponse

def count_tickets_in_window(tickets, days: int) -> int:
    return sum(1 for t in tickets if t.days_ago <= days)

def has_complaint_ticket(tickets) -> bool:
    return any(t.category.lower() == "complaint" for t in tickets)

def evaluate_churn_risk(customer: CustomerRequest) -> RiskResponse:
    reasons = []
    tickets_30d = count_tickets_in_window(customer.tickets, 30)
    complaint = has_complaint_ticket(customer.tickets)

    # Rule 1: More than 5 tickets in last 30 days → HIGH
    if tickets_30d > 5:
        reasons.append(f"HIGH: {tickets_30d} tickets raised in last 30 days (threshold: 5)")
        return RiskResponse(
            customer_id=customer.customer_id,
            risk_level="HIGH",
            reasons=reasons,
            tickets_last_30_days=tickets_30d,
            has_complaint=complaint,
        )

    # Rule 2: Month-to-Month contract + complaint ticket → HIGH
    if customer.contract_type == "Month-to-Month" and complaint:
        reasons.append("HIGH: Month-to-Month contract with active complaint ticket")
        return RiskResponse(
            customer_id=customer.customer_id,
            risk_level="HIGH",
            reasons=reasons,
            tickets_last_30_days=tickets_30d,
            has_complaint=complaint,
        )

    # Rule 3: 3 or more tickets in last 30 days → MEDIUM
    if tickets_30d >= 3:
        reasons.append(f"MEDIUM: {tickets_30d} tickets in last 30 days (threshold: 3)")
        return RiskResponse(
            customer_id=customer.customer_id,
            risk_level="MEDIUM",
            reasons=reasons,
            tickets_last_30_days=tickets_30d,
            has_complaint=complaint,
        )

    # Default → LOW
    reasons.append("LOW: No significant churn indicators found")
    return RiskResponse(
        customer_id=customer.customer_id,
        risk_level="LOW",
        reasons=reasons,
        tickets_last_30_days=tickets_30d,
        has_complaint=complaint,
    )