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
import os
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
    
    # Admin Access 
    # Added by Zoe Steinkoenig 
    # 12-05-2025
    @app.post("/api/check-admin")
    def check_admin():
        data = request.get_json(silent=True) or {}

        email = data.get("email")
        code = data.get("code")

        if not email or not code:
         return jsonify({"success": False, "message": "email and code required"}), 400

        try:
            query = "SELECT admin_code FROM user WHERE email = %s"
            result = sql_class.run_query(query, (email,))  # use sql_class instance

            if result and len(result) > 0:
                stored_code = result[0][0]  # first column from the SQL query
                if str(stored_code) == str(code):
                    return jsonify({"success": True}), 200
            
            return jsonify({"success": False}), 200

        except Exception as e:
            print("Admin Check Error:", e)
            return jsonify({"success": False, "message": "server error"}), 500

    # Flask Route: Get all Bills
    # Zoe Steinkoenig
    # Added 12-05-2025    
    @app.route("/bills/all")
    def get_all_bills():
        query = """
            SELECT receipt_id, customer_email, total_amount, amount_due, created_at, note
            FROM receipt
            WHERE amount_due > 0  -- only show active bills
            ORDER BY created_at DESC
        """
        result = sql_class.run_query(query)
        return jsonify(result)

    # Flask Route: Get items for a bill (bill page)
    # Zoe Steinkoenig
    # 12-05-2025
    @app.route("/bill/items")
    def get_bill_items():
        receipt_id = request.args.get("receipt_id")

        query = """
            SELECT r.item_line_id, r.item_id, i.item_name, 
                r.quantity, r.item_price, r.item_tax
            FROM receipt_item r
            JOIN inventory_item i ON r.item_id = i.item_id
            WHERE r.receipt_id = %s
        """
        result = sql_class.run_query(query, (receipt_id,))
        return jsonify(result if result else [])

    
    # Flask: New Bill
    # Zoe Steinkoenig
    # 12-05-2025
    @app.post("/bill/create")
    def create_bill():
        try:
            query = """
                INSERT INTO receipt (customer_email, total_amount, amount_due, created_at)
                VALUES (NULL, 0, 0, NOW());
            """

            new_id = sql_class.run_insert(query)
            print("NEW RECEIPT CREATED:", new_id)

            return jsonify({"receipt_id": new_id})

        except Exception as e:
            print("Error creating bill:", e)
            return jsonify({"error": str(e)}), 500

    # Flask Route: Getting inventory Items
    # Zoe Steinkoenig
    # 12-05-2025
    @app.route("/inventory/items", methods=["GET"])
    def get_inventory_items():
        try:
            query = """
                SELECT 
                    item_id,
                    item_name,
                    price,
                    quantity,
                    category_id,
                    tax_rate,
                    avg_rating
                FROM inventory_item;
            """

            result = sql_class.run_query(query)

            # Return EXACTLY the SQL rows as arrays
            return jsonify(result if result else [])

        except Exception as e:
            print("Inventory Error:", e)
            return jsonify([]), 500

        
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
    
    @app.post("/bill/pay")
    def add_payment_method():
        data = request.get_json()

        receipt_id = data.get("receipt_id")
        payment_type = data.get("payment_type")
        amount = float(data.get("amount"))

        # 1. Record the payment
        payment_added = payment_class.add_payment_method(receipt_id, payment_type, amount)

        if not payment_added:
            return jsonify({"success": False})

        # 2. Get current amount_due
        query = "SELECT amount_due FROM receipt WHERE receipt_id = %s"
        result = sql_class.run_query(query, (receipt_id,))

        if not result:
            return jsonify({"success": False})

        current_due = float(result[0][0])
        new_due = max(current_due - amount, 0)

        # 3. Update amount_due in receipt
        update_query = """
            UPDATE receipt
            SET amount_due = %s,
                note = %s
            WHERE receipt_id = %s
        """

        note = "Paid" if new_due == 0 else "Partial Payment"

        sql_class.run_query(update_query, (new_due, note, receipt_id))

        return jsonify({
            "success": True,
            "new_due": new_due,
            "status": note
        })
        
    @app.post("/bill/split")
    def split_payment():
        data = request.get_json()
        receipt_id = data["receipt_id"]
        num_people = data["num_people"]

        success = payment_class.split_payment(receipt_id, num_people)

        return jsonify({"success": bool(success)})

    @app.post("/bill/discount")
    def apply_discount():
        data = request.get_json()
        code = data["coupon"]
        total = data["total"]

        new_total = payment_class.apply_discounts(code, total)

        return jsonify({"success": True, "new_total": new_total})

    @app.post("/bill/tip")
    def add_tip():
        data = request.get_json()
        receipt_id = data["receipt_id"]
        tip_amount = data["tip"]

        success = payment_class.add_tips(receipt_id, tip_amount)

        return jsonify({"success": bool(success)})

    @app.post("/bill/add-item")
    def add_item_to_bill():
        data = request.get_json()
        receipt_id = data["receipt_id"]
        item_id = data["item_id"]
        qty = data["qty"]
        price = data["price"]

        added = payment_class.add_item_to_bill(receipt_id, item_id, qty, price)

        if added:
            payment_class.update_receipt_totals(receipt_id)

        return jsonify({"success": bool(added)})


    @app.post("/bill/remove-item")
    def remove_item_from_bill():
        data = request.get_json()
        receipt_id = data["receipt_id"]
        line_id = data["item_line_id"]

        removed = payment_class.remove_item_from_bill(line_id, receipt_id)

        if removed:
            payment_class.update_receipt_totals(receipt_id)

        return jsonify({"success": bool(removed)})
    
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


    @app.route("/orderAhead")
    def orderAhead():
        item = request.form["oa-item-select"]
        quantity = request.form["oa-qty"]
        time = request.form["oa-pickup-time"]
        ordered = customer_class.order_ahead(item, quantity, time)

        if ordered:
            return render_template ("orderAhead.html")
        else:
            return jsonify({"status": "fail", "message": "could not order ahead"}), 200

    @app.route("/maintenanceRequest", methods=["GET"])
    def maintenance_request_page():
        return render_template("maintenanceRequest.html")

    @app.post("/maintenanceRequest")
    def request_maintance():
        data = request.get_json(silent=True) or {}

        code = data.get("code")
        message = data.get("message")

        requested = manager_class.request_maintance(code, message)

        return jsonify({"success": bool(requested)})

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