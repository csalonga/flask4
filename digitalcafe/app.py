from flask import Flask, flash, redirect
from flask import render_template
from flask import request
from flask import session
import database as db
import authentication
import ordermanagement as om
import logging

app = Flask(__name__)
# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    return render_template('branches.html', page="Branches")

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        flash("Invalid username or password. Please try again.")
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')


@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a
    # quantity of 1 for now

    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]
    item["code"] = request.args.get('code', '')

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')


@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/formsubmission', methods = ['POST', 'GET'])
def form_submission():
    stype = request.form.get("stype")
    if stype == "Delete":        
        cart = session["cart"]
        cart.pop(request.form['code'],None)
        session["cart"] = cart
        print("deleted")

    else:
        code = request.form['code']
        product = db.get_product(int(code))
        item=dict()

        item["qty"] = int(request.form['qty'])
        item["name"] = product["name"]
        item["subtotal"] = product["price"]*item["qty"]
        item["code"] = code

        if(session.get("cart") is None):
            session["cart"]={}

        cart = session["cart"]
        cart[code]=item
        session["cart"]=cart

    return redirect('/cart')

@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)

    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')

@app.route('/orders')
def orders():
    order_list = db.get_orders(session['user'])
    return render_template('orders.html', page="orders", order_list=order_list)

