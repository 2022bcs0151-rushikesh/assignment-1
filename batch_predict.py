import csv
from app.models import CustomerRequest, Ticket, ContractType
from app.rules import evaluate_churn_risk

def load_data():
    customers = {}
    with open("data/customers.csv") as f:
        for row in csv.DictReader(f):
            customers[row["customer_id"]] = row

    tickets = {}
    with open("data/tickets.csv") as f:
        for row in csv.DictReader(f):
            cid = row["customer_id"]
            tickets.setdefault(cid, []).append(row)

    return customers, tickets

def run_batch():
    customers, tickets = load_data()
    results = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    with open("data/predictions.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["customer_id","contract_type","risk_level","tickets_30d","has_complaint"])
        writer.writeheader()

        for cid, c in customers.items():
            ticket_objs = [
                Ticket(
                    ticket_id=t["ticket_id"],
                    days_ago=int(t["days_ago"]),
                    category=t["category"]
                )
                for t in tickets.get(cid, [])
            ]
            request = CustomerRequest(
                customer_id=cid,
                contract_type=c["contract_type"],
                monthly_charge=float(c["monthly_charge"]),
                tickets=ticket_objs,
            )
            result = evaluate_churn_risk(request)
            results[result.risk_level] += 1
            writer.writerow({
                "customer_id": cid,
                "contract_type": c["contract_type"],
                "risk_level": result.risk_level,
                "tickets_30d": result.tickets_last_30_days,
                "has_complaint": result.has_complaint,
            })

    print(f"\nBatch prediction complete — 200 customers processed")
    print(f"HIGH  risk: {results['HIGH']}")
    print(f"MEDIUM risk: {results['MEDIUM']}")
    print(f"LOW   risk: {results['LOW']}")
    print(f"Results saved to data/predictions.csv")

if __name__ == "__main__":
    run_batch()