import csv
import random
import os

random.seed(42)

customers = []
tickets = []

contract_types = ["Month-to-Month", "One Year", "Two Year"]
categories = ["complaint", "billing", "technical", "general"]

for i in range(200):
    customer_id = f"C{i+1:04d}"
    contract = random.choice(contract_types)
    monthly_charge = round(random.uniform(20, 120), 2)
    num_tickets = random.randint(0, 8)

    customers.append({
        "customer_id": customer_id,
        "contract_type": contract,
        "monthly_charge": monthly_charge,
        "num_tickets_30d": num_tickets,
    })

    for j in range(num_tickets):
        tickets.append({
            "ticket_id": f"T{i+1:04d}{j+1:02d}",
            "customer_id": customer_id,
            "days_ago": random.randint(1, 30),
            "category": random.choice(categories),
        })

os.makedirs("data", exist_ok=True)

with open("data/customers.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["customer_id","contract_type","monthly_charge","num_tickets_30d"])
    writer.writeheader()
    writer.writerows(customers)

with open("data/tickets.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["ticket_id","customer_id","days_ago","category"])
    writer.writeheader()
    writer.writerows(tickets)

print("Generated 200 customers and ticket logs in data/")