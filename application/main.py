from data.backend_sql import Backend as sql
from Backend.customer import Customer as cust
from Backend.inventory import Inventory as invent
from Backend.manager import Manager as man
from Backend.payment import Payment as pay
from Backend.user_account import Account as acc
from dotenv import load_dotenv # you have to import dotenv (see dependencies.txt file)
import os
from flask import jsonify, request, Flask, render_template # for connecting code to backend

app = Flask(__name__, template_folder="../Frontend/HTML")

# Loads variables from .env in the current directory
load_dotenv()

# Load database credentials from environment
database_host = os.getenv("DB_HOST")
database_user = os.getenv("DB_USER")
database_password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")

# Create class instances.
sql_class = sql.Backend(database_host, database_user, database_password, database)
account_class = acc()
payment_class = pay()
manager_class = man()
inventory_class = invent()
customer_class = cust()


class main:

    """
    Handles user input and menu navigation.
    """

    @app.route("/signup")
    def signup():
        data = request.get_json()
        email = data["signupInfo.email"]
        password = data["signupInfo.password"]
        type = data["signupInfo.user_type"]
        question = data["signupInfo.security_question"]
        answer =data["signupInfo.security_answer"]

        creatred = account_class.create_account(email, password, type, question, answer)

        if creatred:
            return render_template ("signup.html")
        else:
            return jsonify({"status": "fail", "message": "could not create account"}), 200
        
    @app.route("/login")
    def login():
        data = request.get_json()
        email = data["username"]
        password = data["password"]

        logged_in = account_class.log_in(email, password)

        if logged_in [0]:
            return render_template ("login.html")
        else:
            return jsonify({"status": "fail", "message": "could not login"}), 200
        

    @app.route("/settings")
    def logout():
        logged_out = account_class.log_out()

        if logged_out [0]:
            return render_template ("settings.html")
        else:
            return jsonify({"status": "fail", "message": "could not logout"}), 200
        
    @app.route("/resetPassword")
    def reset_password(): 
        data = request.get_json()
        email = data["email"]
        password = data["newPassword"]
        answer = data["securityAnswer"]

        reset = account_class.password_reset(email, password, answer)

        if reset:
            return render_template ("forgotPassword.html")
        else:
            return jsonify({"status": "fail", "message": "could not reset password"}), 200
    
    @app.route("/bill")
    def add_payment_method():
        transaction_id = request.form["reciept-id"]
        payment_type = request.form["payment-method"]
        amount = request.form["payment-amount"]

        payment_added = payment_class.add_payment_method(transaction_id, payment_type, amount)
        
        if payment_added:
            return render_template ("bill.html")
        else:
            return jsonify({"status": "fail", "message": "could not add payment method"}), 200
        
    @app.route("/bill")
    def split_payment():
        data = request.get_json()
        receiptId = data["itemId"]
        numPeople = data["numPeople"]

        payment_split = payment_class(receiptId, numPeople)
        
        if payment_split:
            return render_template ("bill.html")
        else:
            return jsonify({"status": "fail", "message": "could not split payment"}), 200
        
     
    @app.route("/bill")
    def add_discount():
        data = request.get_json()
        code = data["coupon"]
        total = data["total"]

        new_total = payment_class.apply_discounts(code, total)

        if new_total != 0:
            return render_template ("bill.html")
        else:
            return jsonify({"status": "fail", "message": "could not apply discount"}), 200
    
    @app.route("/bill")
    def add_tip():
        data = request.get_json()
        receiptId = data["itemId"]
        tip_amount = data["tip"]

        tip_added = payment_class.add_tips(receiptId, tip_amount)
        
        if tip_added:
            return render_template ("bill.html")
        else:
            return jsonify({"status": "fail", "message": "could not add tip"}), 200

    @app.route("/bill")
    def add_item_to_bill():
        data = request.get_json()
        id = data["itemId"]
        item = data["item"]
        price = data["price"]
        quantity = data["qty"]

        added = payment_class.add_item_to_bill(id, item, price, quantity)
        
        if added:
            return render_template ("bill.html")
        else:
            return jsonify({"status": "fail", "message": "could not add item to bill"}), 200
    
    @app.route("/bill")
    def remove_from_bill():
        pass
    
    @app.route("/bill")
    def void_transaction():
        receiptID = request.form["void-receipt-id"]
        email = request.form["admin-email"]
        code = request.form["admin-code"]

        voided = payment_class.void_transaction(receiptID, email, code)

        if voided:
            return render_template ("bill.html")
        else:
            return jsonify({"status": "fail", "message": "could not void transaction"}), 200

    @app.route("/bill")
    def approve_voided_transaction():
        receiptID = request.form["void-receipt-id"]
        email = request.form["admin-email"]
        code = request.form["admin-code"]

        approved = payment_class.void_transaction(receiptID, email, code)

        if approved:
            return render_template ("bill.html")
        else:
            return jsonify({"status": "fail", "message": "could not approved void transaction"}), 200
        
    @app.route()
    def manage_refunds():
        pass

    @app.route()
    def redeem_points():
        pass

    @app.route()
    def add_to_inventory():
        pass

    @app.route()
    def update_count():
        pass

    @app.route()
    def track_stock():
        pass
    
    @app.route()
    def find_product():
        pass

    @app.route("/index")
    def sales_report(): 
        pass

    @app.route()
    def order_ahead():
        pass

    @app.route()
    def request_maintance():
        pass

    @app.route()
    def print_reciepts():
        pass

    @app.route()
    def rate_items():
        pass

    @app.route()
    def feedback():
        pass

    @app.route()
    def add_categories():
        pass

    @app.route()
    def add_items_to_categories():
        pass