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

    @app.route("/bill")
    def add_to_bill():
        # add_item_to_bill(self, receiptID, item, price, quantity) payment
        # html does not ask for reciptID
        # can you seperate item and price

    @app.route("/bill")
    def add_tip():
        # add_tips(self, receiptID, tip_amount) payment
        # html does not ask for reciptID

    @app.route("/bill")
    def add_discount():
        # apply_discounts(self, discount_percent: int, total: float) payment #change this

    @app.route("/bill")
    def split_payment():
        # split_payment(self, receiptID, numPeople) payment
        # does not ask for reciept id


    @app.route("/bill")
    def add_payment_method():
        # add_payment_method(self, transaction_id, payment_type, amount) payment
        # there seems to be no backend logic to add payment method, need to understand

    @app.route("/index")
    def void_transaction():
        # void_transaction(self, receiptID, admin_email, admin_code) payment
        # does not ask for reciept number, admin_email and code 

    @app.route("/index")
    def approve_voided_transaction():
        # approve_voided_transaction(self, receiptID, adminEmail, code) payment
        # no reciept id, html does not ask for admin email and code

    @app.route("/index")
    def add_item_to_bill():
        # add_item_to_bill(self, receiptID, item, price, quantity) payment
        #there's no place to input bill id (it a hard coded string)
        # need name field in the html (can't use id)

    @app.route("/index") # not yet implemented
    def sales_report():
        # view_sales_report(self) manager

    @app.route("/index") #done
    def logout():
        logged_out = account_class.log_out()

        if logged_out [0]:
            return render_template ("index.html")
        else:
            return jsonify({"status": "fail", "message": "could not logout"}), 200

    @app.route("/login") # done
    def login():
        email = request.form["email"]
        password = request.form["password"]

        logged_in = account_class.log_in(email, password)

        if logged_in [0]:
            return render_template ("login.html")
        else:
            return jsonify({"status": "fail", "message": "could not login"}), 200

    @app.route("/signup") #Check (CV)
    def signup():
        # create_account(self, email, password, user_type, security_question, security_answer) account

        # no field for user_type and security question and answer
        # ^^Implemented now double check to make sure, It gets the network error but thats because the flask isnt set up yet Frontend should be good

    @app.route("/resetPassword")
    def reset_password(): 
        # password_reset(self, email, new_password, security_answer) account
        
        # 2 reset password pages
        # ^^ Marked one for delete, want a double check before deleting(CV)
        # use current logged in email for email
        # is there a way to check if password are the same in html or js?
        # no field for security answer


    # right now reset password has 2 different pages, ask to be fixed (make reset password button go to reset password.html) using the reset password.html
    # nothing for remove item from bill
    # nothing for manage refund
    # nothing for redeem loyalty point
    # nothing for get security question
    # nothing for manage refund
    # please make sure there is a name field in the html (that how i get info into database, cant use id)