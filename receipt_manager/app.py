from flask import Flask, render_template, request, redirect, url_for
from database import db, Receipt, app

# Route to list all receipts
@app.route('/receipts')
def receipt_list():
    receipts = db.session.execute(db.select(Receipt).order_by(Receipt.date)).scalars()
    return render_template('receipt/list.html', receipts=receipts)

# Route to create a new receipt
@app.route('/receipts/create', methods=['GET', 'POST'])
def receipt_create():
    if request.method == 'POST':
        # Create a new receipt object from the form data
        receipt = Receipt(
            date=request.form['date'],
            company=request.form['company'],
            price=float(request.form['price'])
        )
        # Add the receipt to the database session and commit
        db.session.add(receipt)
        db.session.commit()
        # Redirect to the receipt list page
        return redirect(url_for('receipt_list'))
    # Render the create receipt form
    return render_template('receipt/create.html')

# Route to view receipt details
@app.route('/receipt/<int:id>')
def receipt_detail(id):
    # Fetch the receipt by ID, 404 if not found
    receipt = db.get_or_404(Receipt, id)
    return render_template('receipt/detail.html', receipt=receipt)

# Route to delete a receipt
@app.route('/receipt/<int:id>/delete', methods=['GET', 'POST'])
def receipt_delete(id):
    # Fetch the receipt by ID, 404 if not found
    receipt = db.get_or_404(Receipt, id)
    if request.method == 'POST':
        # Delete the receipt and commit the change
        db.session.delete(receipt)
        db.session.commit()
        # Redirect to the receipt list page
        return redirect(url_for('receipt_list'))
    # Render the delete confirmation form
    return render_template('receipt/delete.html', receipt=receipt)

if __name__ == '__main__':
    app.run(debug=True)
