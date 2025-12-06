import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.backend_sql import Backend as sql
from Backend.customer import Customer as cust
from Backend.inventory import Inventory as invent
from Backend.manager import Manager as man
from Backend.payment import Payment as pay
from Backend.user_account import Account as acc
from dotenv import load_dotenv # you have to import dotenv (see dependencies.txt file)
from flask import jsonify, request, Flask, render_template # for connecting code to backend

app = Flask(__name__, template_folder="../Frontend/HTML", static_folder="../Frontend/static")

# Loads variables from .env in the current directory
load_dotenv()

# Load database credentials from environment
database_host = os.getenv("DB_HOST")
database_user = os.getenv("DB_USER")
database_password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")

# Create class instances.
sql_class = sql(database_host, database_user, database_password, database)
account_class = acc()
payment_class = pay()
manager_class = man()
inventory_class = invent()
customer_class = cust()


class main:
    @app.route("/")
    def index():
        """Home page route."""
        return render_template("index.html")

    @app.route("/settings", methods=["GET", "POST"])
    def settings():
        if request.method == "POST":
            customer_email = request.form.get("customer_email")
            feedback = request.form.get("feedbackInput")
            if customer_email and feedback:
                recived = customer_class.give_feedback(customer_email, feedback)
                if recived.get("success"):
                    return render_template("settings.html")
                else:
                    return jsonify({"status": "fail", "message": recived.get("message", "Feedback error")}), 200
        return render_template("settings.html")

    @app.route("/admin", methods=["GET"])
    def admin():
        return render_template("admin.html")

    @app.route("/inventory", methods=["GET"])
    def inventory():
        return render_template("inventory.html")

    @app.route("/orderAhead", methods=["GET"])
    def order_ahead_page():
        return render_template("orderAhead.html")

    @app.route("/bill", methods=["GET"])
    def bill():
        return render_template("bill.html")

    @app.route("/bills", methods=["GET"])
    def bills():
        return render_template("bills.html")

    @app.route("/sales", methods=["GET"])
    def sales():
        return render_template("sales.html")

    @app.route("/maintenanceRequest", methods=["GET"])
    def maintenance_request():
        return render_template("maintenanceRequest.html")

    @app.route("/forgotPassword", methods=["GET"])
    def forgot_password():
        return render_template("forgotPassword.html")
    @app.route("/inventory/items")
    def get_inventory_items():
        items = sql_class.run_query("SELECT item_id, item_name, price, quantity, category_id FROM inventory_item")
        return jsonify(items)

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
        
    @app.route("/forgotPassword")
    def reset_password():
        data = request.get_json()
        email = data["email"]
        password = data["newPassword"]
        answer = data["securityAnswer"]

        reset = account_class.password_reset(email, password, answer)

        if reset:
            return render_template("forgotPassword.html")
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
        data = request.get_json()
        id = data["itemId"]
        item = data["item"]
        removed = payment_class.remove_item_from_bill(id, item)
        if removed:
            return render_template("bill.html")
        else:
            return jsonify({"status": "fail", "message": "could not remove item from bill"}), 200
    
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
        
    @app.route("/bill/refund")
    def manage_refunds():
        data = request.get_json()
        admin_code = data["admin_code"]
        admin_email = data["admin_email"]
        total_due = data["total_due"]
        refund_amount = data["refund_amount"]
        receipt_id = data["receipt_id"]
        refunded = payment_class.manage_refund(admin_code, admin_email, total_due, refund_amount, receipt_id)
        if refunded:
            return render_template("bill.html")
        else:
            return jsonify({"status": "fail", "message": "could not process refund"}), 200

    @app.route("/bills")
    def redeem_points():
        email = request.form["loyalty-email"]
        points = request.form["redeem-points"]
        redeemed = customer_class.redeem_loyalty_point(email, points)

        if redeemed:
            return render_template ("bill.html")
        else:
            return jsonify({"status": "fail", "message": "could not redeem points"}), 200

    @app.route("/inventory")
    def add_to_inventory():
        name = request.form["new-item-name"]
        price = request.form["new-item-price"]
        quant = request.form["new-item-qty"]
        cat = request.form["new-item-category"]

        added = inventory_class.add_to_inventory(name, price, quant, cat)

        if added:
            return render_template ("inventory.html")
        else:
            return jsonify({"status": "fail", "message": "could not add to inventory"}), 200

    @app.route("/inventory/update")
    def update_count():
        data = request.get_json()
        product_name = data["product_name"]
        price = data["price"]
        quantity = data["quantity"]
        category = data["category"]
        updated = inventory_class.update_product(product_name, price, quantity, category)
        if updated:
            return render_template("inventory.html")
        else:
            return jsonify({"status": "fail", "message": "could not update product"}), 200

    @app.route("/inventory/track")
    def track_stock():
        lowStock_limit = request.args.get("lowStock_limit", 4)
        tracked = inventory_class.track_inventory(lowStock_limit)
        if tracked:
            return render_template("inventory.html")
        else:
            return jsonify({"status": "fail", "message": "could not track inventory"}), 200
    
    @app.route("/inventory")
    def find_product():
        name = request.form["inventory-search"]

        found = inventory_class.find_product(name)
        
        if found:
            return render_template ("inventory.html")
        else:
            return jsonify({"status": "fail", "message": "could not find product"}), 200

    @app.route("/sales")
    def sales_report(): 
        unlocked = report.form["is_unlocked"]

        if unlocked:
            report = manager_class.view_sales_report()
            if report:
                return render_template ("sales.html")
        
        return jsonify({"status": "fail", "message": "could not view report"}), 200

    @app.route("/orderAhead", methods=["POST"])
    def orderAhead_submit():
        try:
            data = request.get_json()
            customer_email = data.get("customer_email")
            items = data.get("items")           # [{item_name, quantity}, ...]
            note = data.get("note")             # e.g., pickup time

            # If your current `order_ahead` handles only one item, loop through items
            for item in items:
                success = customer_class.order_ahead(customer_email, item["item_name"], item["quantity"], note)
                if not success:
                    return jsonify({"success": False, "message": f"Failed to add {item['item_name']}"})

            return jsonify({"success": True, "message": "Order placed!"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

    @app.route("/maintenance")
    def request_maintance():
        data = request.get_json()
        code = data["code"]
        message = data["message"]
        requested = manager_class.request_maintance(code, message)
        if requested:
            return render_template("maintenanceRequest.html")
        else:
            return jsonify({"status": "fail", "message": "could not request maintenance"}), 200

    @app.route("/bills/print")
    def print_reciepts():
        receipt_id = request.form["receipt-id"]
        printed = manager_class.print_reciept(receipt_id)
        if printed:
            return render_template("bills.html")
        else:
            return jsonify({"status": "fail", "message": "could not print receipt"}), 200

    @app.route("/rate")
    def rate_items():
        data = request.get_json()
        customer_email = data["customer_email"]
        item_name = data["item_name"]
        rating = data["rating"]
        rated = customer_class.rate_item(customer_email, item_name, rating)
        if rated["success"]:
            return render_template("bill.html")
        else:
            return jsonify({"status": "fail", "message": rated["message"]}), 200

    @app.route("/settings")
    def feedback():
        customer_email = request.form["customer_email"]
        feedback = request.form["feedbackInput"]
        recived = customer_class.give_feedback(customer_email, feedback)
        if recived["success"]:
            return render_template("settings.html")
        else:
            return jsonify({"status": "fail", "message": recived["message"]}), 200
        

    @app.route("/inventory/category")
    def add_categories():
        category_name = request.form["category_name"]
        added = inventory_class.add_categories(category_name)
        if added:
            return render_template("inventory.html")
        else:
            return jsonify({"status": "fail", "message": "could not add category"}), 200

    @app.route("/inventory/category/add")
    def add_items_to_categories():
        item_ID = request.form["item_ID"]
        category = request.form["category"]
        added = inventory_class.add_item_to_category(item_ID, category)
        if added:
            return render_template("inventory.html")
        else:
            return jsonify({"status": "fail", "message": "could not add item to category"}), 200
        
    @app.route("/admin/users", methods=["GET"])
    def get_admin_users():
        try:
            users = sql_class.run_query("SELECT email, user_type, security_question, security_answer FROM user_account")
            if not users:
                users = []
            user_list = [
                {
                    "email": u[0],
                    "user_type": u[1],
                    "security_question": u[2],
                    "security_answer": u[3]
                } for u in users
            ]
            return jsonify(user_list)
        except Exception as e:
            print("Error fetching admin users:", e)
            return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500

    
if __name__ == "__main__":
    app.run(debug=True)

    # cant find a place to reset password from index.html
    # cant find where to request refund on frontend
    # for order ahead - do not need order id and need a way to remove items after adding items
    # can't find where to update product count
    # you can request maintance without admin code (should also take message) in frontend and request maintance page is blank
    # can't find where to print reciept
    # can't find where to add category or add item to category
    # item can only be rated on order ahead (maybe seperate page for rate items)
    # can't find where to update product count or track inventory stock