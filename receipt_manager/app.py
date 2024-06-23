from flask import Flask, render_template, request, redirect, url_for
from database import db, Receipt, app

@app.route('/')
def index():
    return redirect(url_for('receipt_list'))

# Route to list all receipts
@app.route('/receipts')
def receipt_list():
    receipts = db.session.execute(db.select(Receipt).order_by(Receipt.date)).scalars()
    return render_template('receipt/list.html', receipts=receipts)

# Route to create a new receipt
@app.route('/receipts/create', methods=['GET', 'POST'])
def receipt_create():
    if request.method == 'POST':
        receipt = Receipt(
            date=request.form['date'],
            company=request.form['company'],
            price=float(request.form['price'])
        )
        db.session.add(receipt)
        db.session.commit()
        return redirect(url_for('receipt_list'))
    return render_template('receipt/create.html')

# Route to view receipt details
@app.route('/receipt/<int:id>')
def receipt_detail(id):
    receipt = db.get_or_404(Receipt, id)
    return render_template('receipt/detail.html', receipt=receipt)

# Route to delete a receipt
@app.route('/receipt/<int:id>/delete', methods=['GET', 'POST'])
def receipt_delete(id):
    receipt = db.get_or_404(Receipt, id)
    if request.method == 'POST':
        db.session.delete(receipt)
        db.session.commit()
        return redirect(url_for('receipt_list'))
    return render_template('receipt/delete.html', receipt=receipt)

if __name__ == '__main__':
    app.run(debug=True)
