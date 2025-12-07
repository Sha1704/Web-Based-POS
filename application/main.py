import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.backend_sql import Backend as sql
from Backend.customer import Customer as cust
from Backend.inventory import Inventory as invent
from Backend.manager import Manager as man
from Backend.payment import Payment as pay
from Backend.user_account import Account as acc
from dotenv import load_dotenv
from flask import *

app = Flask(__name__, template_folder="../Frontend/HTML", static_folder="../Frontend/static")
account = acc()

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
    
    @app.route("/feedback/get", methods=["GET"])
    def get_feedback():
        query = "SELECT feedback_id, message, created_at FROM customer_feedback ORDER BY created_at DESC"
        result = sql_class.run_query(query)
        feedback_list = [
            {"id": r[0], "feedback": r[1], "created_at": str(r[2])} for r in result
        ] if result else []
        return jsonify(feedback_list), 200

    @app.route("/feedback/add", methods=["POST"])
    def add_feedback():
        data = request.get_json() or {}
        message = data.get("feedback")
        
        if not message:
            return jsonify({"success": False, "message": "Feedback message is required"}), 400

        query = "INSERT INTO customer_feedback (message, created_at) VALUES (%s, NOW())"
        new_id = sql_class.run_insert(query, (message,))
        
        return jsonify({"success": True, "id": new_id}), 200

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

    @app.route("/forgotPassword", methods=["GET"])
    def forgot_password():
        return render_template("forgotPassword.html")
    
    @app.route("/inventory/items")
    def get_inventory_items():
        query = """
            SELECT i.item_id,
            i.item_name AS name,
            i.quantity AS quant,
            i.price,
            c.category_name AS category
        FROM inventory_item i
        LEFT JOIN category c ON i.category_id = c.category_id;
        """
        items = sql_class.run_query(query)
        return jsonify(items)

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "GET":
            return render_template("signup.html")

        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        try:
            email = data["email"]
            password = data["password"]
            user_type = data["user_type"]
            question = data["security_question"]
            answer = data["security_answer"]
        except KeyError as e:
            return jsonify({"error": f"Missing field: {str(e)}"}), 400

        created = account_class.create_account(
            email,
            password,
            user_type,
            question,
            answer
        )

        if created:
            return jsonify({"message": "Account created successfully"}), 200
        else:
            return jsonify({"error": "Account creation failed"}), 400
        
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            logged_in = account_class.log_in(email, password)

            if logged_in[0]:
                return redirect(url_for("index"))
            else:
                return jsonify({"status": "fail", "message": "could not login"}), 401

        return render_template("login.html")

    @app.route("/get-security-question", methods=["POST"])
    def get_security_question():
        data = request.get_json() or {}
        email = data.get("email", "").strip().lower()
        
        if not email:
            return jsonify({"error": "Email is required"}), 400

        try:
            query = "SELECT security_question FROM user WHERE email = %s"
            result = sql_class.run_query(query, (email,))
            
            if result and len(result) > 0:
                question = result[0][0]
                return jsonify({"question": question}), 200
            else:
                return jsonify({"error": "Email not found"}), 404
        except Exception as e:
            print("Error fetching security question:", e)
            return jsonify({"error": "Server error"}), 500
        
    @app.route("/logout")
    def logout():
        account.log_out()
        return redirect(url_for('login'))
        
    @app.route("/forgotPassword", methods=["POST"])
    def reset_password():
        data = request.get_json()
        email = data["email"]
        password = data["newPassword"]
        answer = data["securityAnswer"]

        reset = account_class.password_reset(email, password, answer)

        if reset:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "fail", "message": "could not reset password"}), 400

    
    @app.post("/bill/pay")
    def add_payment_method():
        data = request.get_json()

        receipt_id = data.get("receipt_id")
        payment_type = data.get("payment_type")
        amount = float(data.get("amount"))

        payment_added = payment_class.add_payment_method(receipt_id, payment_type, amount)

        if not payment_added:
            return jsonify({"success": False})

        query = "SELECT amount_due FROM receipt WHERE receipt_id = %s"
        result = sql_class.run_query(query, (receipt_id,))

        if not result:
            return jsonify({"success": False})

        current_due = float(result[0][0])
        new_due = max(current_due - amount, 0)

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
        try:
            data = request.get_json()

            receipt_id = data["receipt_id"]
            line_id = data["item_line_id"]

            removed = payment_class.remove_item_from_bill(line_id, receipt_id)

            if removed:
                payment_class.update_receipt_totals(receipt_id)
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False, "message": "Item not removed"}), 400

        except Exception as e:
            print("REMOVE ITEM ERROR:", e)
            return jsonify({"success": False, "message": str(e)}), 500

    @app.route("/inventory/add", methods=["POST"])
    def add_to_inventory():
        data = request.get_json()
        name = data["item_name"]
        price = data["price"]
        quantity = data["quantity"]
        category_id = data["category_id"]

        added = inventory_class.add_to_inventory(name, price, quantity, category_id)

        if added:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "fail", "message": "Could not add item"}), 500

    @app.route("/inventory/update", methods=["POST"])
    def update_product():
        data = request.get_json()

        item_id = data["id"]
        product_name = data["product_name"]
        price = data["price"]
        quantity = data["quantity"]
        category_id = data["category"]

        updated = inventory_class.update_product(
            item_id,
            product_name,
            price,
            quantity,
            category_id
        )

        if updated:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "fail", "message": "Could not update product"}), 500

    @app.route("/inventory/delete", methods=["POST"])
    def delete_inventory_item():
        item_id = request.args.get("id")
        if not item_id:
            return jsonify({"status": "fail", "message": "No item ID provided"}), 400

        deleted = inventory_class.delete_item(item_id)
        if deleted:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "fail", "message": "Could not delete item"}), 500


    @app.route("/inventory/track")
    def track_stock():
        lowStock_limit = request.args.get("lowStock_limit", 4)
        tracked = inventory_class.track_inventory(lowStock_limit)
        if tracked:
            return render_template("inventory.html")
        else:
            return jsonify({"status": "fail", "message": "could not track inventory"}), 200
    
    @app.route("/inventory/get")
    def get_inventory_item():
        item_id = request.args.get("id")
        if not item_id:
            return jsonify({"status": "fail", "message": "No item ID provided"}), 400
        try:
            item_id = int(item_id)
        except ValueError:
            return jsonify({"status": "fail", "message": "Invalid item ID"}), 400
        query = "SELECT i.item_id, i.item_name, i.quantity, i.price, c.category_name AS category " \
                "FROM inventory_item i LEFT JOIN category c ON i.category_id = c.category_id " \
                "WHERE i.item_id = %s"
        result = sql_class.run_query(query, (item_id,))
        if not result:
            return jsonify({"status": "fail", "message": "Item not found"}), 404
        item_row = result[0]
        item = {
            "item_id": item_row[0],
            "item_name": item_row[1],
            "quantity": item_row[2],
            "price": item_row[3],
            "category": item_row[4],
        }
        return jsonify(item), 200

    @app.route("/inventory")
    def find_product():
        name = request.form["inventory-search"]
        found = inventory_class.find_product(name)        
        if found:
            return render_template ("inventory.html")
        else:
            return jsonify({"status": "fail", "message": "could not find product"}), 200

    @app.route("/orderAhead", methods=["POST"])
    def orderAhead_submit():
        try:
            data = request.get_json()
            items = data.get("items")           
            note = data.get("note")             
            result = customer_class.order_ahead(items, note)
            if result.get("success"):
                return jsonify({"success": True, "message": "Order placed!"}) 
            else:
                return jsonify({"success": False, "message": result.get("message")})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

    @app.route("/maintenanceRequest", methods=["GET"])
    def maintenance_request_page():
        return render_template("maintenanceRequest.html")

    @app.route("/maintenance", methods=["GET"])
    def get_maintenance_requests():
        query = """
            SELECT maintenance_id, created_at, order_details AS message
            FROM maintenance
            ORDER BY created_at DESC
        """
        result = sql_class.run_query(query)
        return jsonify(result if result else [])
    
    @app.route("/maintenance/delete/<int:maintenance_id>", methods=["DELETE"])
    def delete_maintenance(maintenance_id):
        try:
            query = "DELETE FROM maintenance WHERE maintenance_id = %s"
            sql_class.run_query(query, (maintenance_id,))
            return jsonify({"success": True}), 200
        except Exception as e:
            print("Delete Maintenance Error:", e)
            return jsonify({"success": False, "message": str(e)}), 500

    @app.post("/maintenanceRequest")
    def request_maintance():
        data = request.get_json(silent=True) or {}
        message = data.get("message")
        if not message:
            return jsonify({"success": False, "message": "Message is required"}), 400
        query = "INSERT INTO maintenance (created_at, order_details) VALUES (NOW(), %s)"
        new_id = sql_class.run_insert(query, (message,))
        
        return jsonify({"success": True, "maintenance_id": new_id})


    @app.route("/bills/print")
    def print_reciepts():
        receipt_id = request.form["receipt-id"]
        printed = manager_class.print_reciept(receipt_id)
        if printed:
            return render_template("bills.html")
        else:
            return jsonify({"status": "fail", "message": "could not print receipt"}), 200

    @app.route("/rate", methods=["POST"])
    def rate_items():
        try:
            if request.is_json:
                data = request.get_json()
                customer_email = data.get("customer_email")
                item_name = data.get("item_name")
                rating = data.get("rating")
            else:
                customer_email = request.form.get("customer_email")
                item_name = request.form.get("item_name")
                rating = request.form.get("rating")
            if not customer_email or not item_name or not rating:
                return jsonify({"success": False, "message": "Missing data"}), 400
            try:
                rating = int(rating)
            except Exception:
                pass
            rated = customer_class.rate_item(customer_email, item_name, rating)
            if isinstance(rated, dict):
                success = rated.get("success", False)
                message = rated.get("message", "Rating result")
            else:
                success = bool(rated)
                message = "Rating submitted" if success else "Rating failed"
            if success:
                if request.is_json:
                    return jsonify({"success": True, "message": message}), 200
                return render_template("bill.html")
            else:
                return jsonify({"success": False, "message": message}), 200
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
        
    @app.route("/settings")
    def feedback():
        customer_email = request.form["customer_email"]
        feedback = request.form["feedbackInput"]
        recived = customer_class.give_feedback(customer_email, feedback)
        if recived["success"]:
            return render_template("settings.html")
        else:
            return jsonify({"status": "fail", "message": recived["message"]}), 200
        
    @app.route("/inventory/categories", methods=["GET"])
    def get_categories():
        rows = sql_class.run_query("SELECT category_id, category_name FROM category")
        return jsonify(rows), 200

    @app.route("/inventory/category", methods=["POST"])
    def add_category():
        data = request.get_json()
        category_name = data.get("category_name")
        
        if not category_name:
            return jsonify({"status": "fail", "message": "No category name provided"}), 400

        added = inventory_class.add_categories(category_name)
        if added:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "fail", "message": "Could not add category"}), 500


    @app.route("/inventory/category/add")
    def add_items_to_categories():
        item_ID = request.form["item_ID"]
        category = request.form["category_name"]
        added = inventory_class.add_item_to_category(item_ID, category)
        if added:
            return render_template("inventory.html")
        else:
            return jsonify({"status": "fail", "message": "could not add item to category"}), 200
        
    @app.route("/inventory/category/delete", methods=["POST"])
    def delete_category():
        data = request.get_json()
        category_id = data.get("category_id")

        if not category_id:
            return jsonify({"status": "fail", "message": "No category ID provided"}), 400

        deleted = inventory_class.delete_category(category_id)
        if deleted:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "fail", "message": "Could not delete category"}), 500

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
       
@app.route("/sales/report", methods=["GET"])
def sales_report_api():
    try:
        query = """
            SELECT receipt_id, customer_email, total_amount, created_at
            FROM receipt
            ORDER BY created_at DESC
        """
        rows = sql_class.run_query(query) or []

        sales = []
        for r in rows:
            sales.append({
                "receipt_id": int(r[0]),
                "customer_email": r[1],
                "total_amount": float(r[2]) if r[2] is not None else 0.0,
                "created_at": r[3].isoformat() if hasattr(r[3], "isoformat") else str(r[3]),
            })

        return jsonify(sales), 200

    except Exception as e:
        print("Sales report API error:", e)
        return jsonify([]), 500

    
if __name__ == "__main__":
    app.run(debug=True)