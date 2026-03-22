from fastapi import FastAPI, HTTPException
from app.models import CustomerRequest, RiskResponse
from app.rules import evaluate_churn_risk
from app.logger import get_logger

logger = get_logger("churn-api")

app = FastAPI(
    title="Telecom Churn Risk API",
    description="Rule-based churn risk prediction engine (Stage 1 - DevOps)",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "stage": "DevOps - Rule Engine"}

@app.post("/predict-risk", response_model=RiskResponse)
def predict_risk(customer: CustomerRequest):
    logger.info(f"Received prediction request for customer: {customer.customer_id}")
    try:
        result = evaluate_churn_risk(customer)
        logger.info(
            f"Customer {customer.customer_id} → Risk: {result.risk_level} | "
            f"Tickets(30d): {result.tickets_last_30_days} | Complaint: {result.has_complaint}"
        )
        return result
    except Exception as e:
        logger.error(f"Error processing customer {customer.customer_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Telecom Churn Risk API is running", "docs": "/docs"}