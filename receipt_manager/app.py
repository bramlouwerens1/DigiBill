from flask import Flask, render_template, request, redirect, url_for
from database import db, Receipt, Product, app




@app.route('/')
def index():
    """
    Renders the home.html template.

    Returns:
        The rendered home.html template.
    """
    return render_template('home.html')


@app.route('/receipts')
def receipt_list():
    """
    Retrieve a list of receipts from the database and render them in a template.

    Returns:
        The rendered template with the list of receipts.
    """
    sort_order = request.args.get('sort', 'new')
    if sort_order == 'old':
        receipts = db.session.execute(db.select(Receipt).order_by(Receipt.date.asc())).scalars()
    else:
        receipts = db.session.execute(db.select(Receipt).order_by(Receipt.date.desc())).scalars()
    return render_template('receipt/list.html', receipts=receipts, sort_order=sort_order)



@app.route('/receipts/create', methods=['GET', 'POST'])
def receipt_create():
    """
    Create a new receipt in the database.

    This function handles the creation of a new receipt by processing the form data
    submitted via a POST request. It creates a new Receipt object with the provided
    date, company, and price, and adds it to the database. It also processes the
    product data dynamically by iterating over the form fields and creating Product
    objects for each product name and quantity provided.

    Returns:
        A redirect response to the receipt_list route.

    Raises:
        None.
    """
    if request.method == 'POST':
        # Call the class receipt to make a new receipt
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
                # Call the class product to make a new product
                product = Product(name=product_name, quantity=product_quantity, receipt_id=receipt.id)
                db.session.add(product)
            product_index += 1
        db.session.commit()
        return redirect(url_for('receipt_list'))
    return render_template('receipt/create.html')


@app.route('/receipt/<int:id>')
def receipt_detail(id):
    """
    Retrieve the details of a receipt and its associated products.

    Args:
        id: The ID of the receipt to retrieve.

    Returns:
        The rendered HTML template with the receipt and its products.

    Raises:
        werkzeug.exceptions.NotFound: If the receipt with the given ID does not exist in the database.
    """
    # Get the receipt with the given ID
    receipt = db.get_or_404(Receipt, id)
    # Show products associated with the receipt
    products = Product.query.filter_by(receipt_id=id).all()
    return render_template('receipt/detail.html', receipt=receipt, products=products)


@app.route('/receipt/<int:id>/delete', methods=['GET', 'POST'])
def receipt_delete(id):
    """
    Delete a receipt from the database.

    Args:
        id: The ID of the receipt to be deleted.

    Returns:
        redirect: A redirect to the receipt list page.

    Raises:
        404: If the receipt with the given ID does not exist.

    """
    receipt = db.get_or_404(Receipt, id)
    if request.method == 'POST':
        db.session.delete(receipt)
        db.session.commit()
        return redirect(url_for('receipt_list'))
    return render_template('receipt/delete.html', receipt=receipt)

if __name__ == '__main__':
    app.run(debug=True)
