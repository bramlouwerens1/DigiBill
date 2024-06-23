from database import db, Receipt, app

def add_receipt(date, company, price):
    with app.app_context():
        new_receipt = Receipt(date=date, company=company, price=price)
        db.session.add(new_receipt)
        db.session.commit()
        print("Receipt added successfully")

# Simulate a trigger
add_receipt("2024-06-22", "Store A", 20.00)
