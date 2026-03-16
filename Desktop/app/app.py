from flask import Flask, render_template, request,url_for,redirect
from connections import session
from models import Products

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
      
        pname = request.form['pname']
        qty = request.form['qty']

        new_product = Products(pname, qty)
        session.add(new_product)
        session.commit()
    


    return render_template('index.html')

@app.route("/view")
def view():
    items=session.query(Products).all()
    return render_template("view.html",items=items)


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    product = session.query(Products).get(id)
    if not product:
        return "Product not found!", 404

    if request.method == 'POST':
        product.pname = request.form['pname']  
        product.qty = request.form['qty']
        session.commit()
        return redirect('/')

    return render_template('edit.html', product=product)

@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    product = session.query(Products).get(id)
    session.delete(product)
    session.commit()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)