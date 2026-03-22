# Telecom Churn Risk API — Stage 1 (DevOps)

Rule-based churn prediction microservice for the MLOps Assignment.

## How to run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for the interactive API documentation.

## Run with Docker
```bash
docker-compose up --build
```

## Run tests
```bash
pytest tests/ -v
```

## API endpoint

**POST /predict-risk**

Example request:
```json
{
  "customer_id": "C001",
  "contract_type": "Month-to-Month",
  "monthly_charge": 75.0,
  "tickets": [
    {"ticket_id": "T1", "days_ago": 5, "category": "complaint"},
    {"ticket_id": "T2", "days_ago": 10, "category": "technical"},
    {"ticket_id": "T3", "days_ago": 20, "category": "billing"}
  ]
}
```

Example response:

```json
{
  "customer_id": "C001",
  "risk_level": "HIGH",
  "reasons": ["HIGH: Month-to-Month contract with active complaint ticket"],
  "tickets_last_30_days": 3,
  "has_complaint": true
}
```

## Business rules

| Rule | Condition | Risk |
|------|-----------|------|
| 1 | Tickets in last 30 days > 5 | HIGH |
| 2 | Month-to-Month + complaint ticket | HIGH |
| 3 | Tickets in last 30 days ≥ 3 | MEDIUM |
| 4 | None of the above | LOW |