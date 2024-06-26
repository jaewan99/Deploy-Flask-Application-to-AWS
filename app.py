from flask import Flask,redirect
from flask import render_template
from flask import request
import database as db
import authentication
import logging
from flask import session
import ordermanagement as om
from bson.json_util import loads, dumps
from flask import make_response

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
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches", branch_list=branch_list)

@app.route('/branchdetails')
def branchdetails():
    code = request.args.get('code', '')
    branch = db.get_branch(code)
    print(branch)
    return render_template('branchdetails.html', code=code, branch=branch)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/auth', methods = ['POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user, errorMessage = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return render_template('login.html', errorMessage=errorMessage)

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
    # item["code"] = product["code"]
    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/formsubmission', methods = ['POST'])
def form_submission():
    stype = request.form.get("stype")
    if stype == "Update":
        qty = request.form.getlist("qty")
        code = request.form.getlist("code")
        cart = session["cart"]
        for i in range(len(qty)):
            cart[code[i]]["qty"] = (qty[i])
            cart[code[i]]["subtotal"] = (int(qty[i]))*(db.get_product(int(code[i]))["price"])
        session["cart"] = cart
    return redirect('/cart')


@app.route('/del_cart_item/<int:code>')
def del_cart_item(code):
    code = str(code)
    cart = session["cart"]
    cart.pop(code)
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


@app.route('/previousorder')
def previousorder():
    order_list = db.get_user_orders()
    return render_template('previousorder.html', order_list=order_list)

@app.route('/changepassword')
def changepassword():
    return render_template('changepassword.html')

@app.route('/userchangepassword', methods = ['POST'])
def userchangepassword():
    stype = request.form.get("stype")
    if stype == "Update":
        oldpwd = request.form.get("pwd")
        newpwd = request.form.get("pwdnew")
        renewpwd = request.form.get("pwdnewre")
        if oldpwd == db.get_user_password(session["user"]["username"]):
            if newpwd == renewpwd:
                db.change_user_password(newpwd)
                return redirect('/')
            else:
                return redirect('/changepassword')
    return redirect('/changepassword')


@app.route('/api/products/<int:code>',methods=['GET'])
def api_get_product(code):
    resp = make_response(dumps(db.api_get_product(code)))
    resp.mimetype = 'application/json'
    return resp
