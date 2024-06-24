from flask import Flask, render_template, request, redirect, url_for
from database import db, Receipt, Product, app

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/receipts')
def receipt_list():
    receipts = db.session.execute(db.select(Receipt).order_by(Receipt.date)).scalars()
    return render_template('receipt/list.html', receipts=receipts)

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
        
        product_index = 1
        while f'product_name_{product_index}' in request.form:
            product_name = request.form[f'product_name_{product_index}']
            product_quantity = int(request.form[f'product_quantity_{product_index}'])
            if product_name and product_quantity:
                product = Product(name=product_name, quantity=product_quantity, receipt_id=receipt.id)
                db.session.add(product)
            product_index += 1
        db.session.commit()
        
        return redirect(url_for('receipt_list'))
    return render_template('receipt/create.html')

@app.route('/receipt/<int:id>')
def receipt_detail(id):
    receipt = db.get_or_404(Receipt, id)
    products = Product.query.filter_by(receipt_id=id).all()
    return render_template('receipt/detail.html', receipt=receipt, products=products)

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
