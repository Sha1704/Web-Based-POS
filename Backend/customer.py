from data import backend_sql as sql # for sql queries
from dotenv import load_dotenv
import os


load_dotenv()

database_host = os.getenv("DB_HOST")
database_user = os.getenv("DB_USER")
database_password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")

# Create backend database handler
backend = sql.Backend(database_host, database_user, database_password, database)

# Ensure correct database is used
backend.run_query('use web_based_pos;')

class Customer:
    def redeem_loyalty_point(self, email, points_to_redeem): # Dariya
        """
        Redeem loyalty points from a customer's account
        Points are deducted if the customer has enough balance.
        """
        points_query = 'SELECT points FROM customer WHERE email = %s'
        customer_data = backend.run_query(points_query, (email,))
        if not customer_data:
            return {"success": False, "message": "Customer not found", "remaining_points": None}
        current_points = customer_data[0][0]
        if current_points < points_to_redeem:
            return {
                "success": False,
                "message": "Not enough points",
                "remaining_points": current_points
            }
        update_query = 'UPDATE customer SET points = %s WHERE email = %s'
        new_points = current_points - points_to_redeem
        backend.run_query(update_query, (new_points, email))
        return {
            "success": True,
            "message": f"Redeemed {points_to_redeem} points",
            "remaining_points": new_points
        }
    
    def order_ahead(self, customer_email, items, tip=0.0, note=None): # Dariya
        """
        The order is completed online by customer and it will create a receipt and transaction
        :param customer_email: email of the customer placing the order
        :param items: list of items to order
        :param tip: tip amount to include in the order (default 0.0)
        :param note: optional note for the receipt
        """
        try:
            if not backend.run_query("SELECT email FROM customer WHERE email = %s;", (customer_email,)):
                return {"success": False, "message": "Customer not found"}
            subtotal = 0
            total_tax =0
            item_data = []
            # validate each item 
            for item in items:
                result = backend.run_query("SELECT item_id, quantity, price, tax_rate FROM inventory_item WHERE item_name = %s;", (item["item_name"],))
                if not result or result[0][1] < item.get("quantity", 1):
                    return {"success": False, "message": f"Not enough {item['item_name']} available"}
                # store item info for later use
                item_data.append({
                    "item_id": result[0][0],
                    "price": float(result[0][2]),
                    "tax_rate": float(result[0][3]),
                    "quantity": item.get("quantity", 1)
                })
            query = "INSERT INTO receipt (customer_email, total_amount, amount_due, note) VALUES (%s, 0, 0, %s);"
            backend.run_query(query, (customer_email, note))
            receipt_id = int(backend.run_query("SELECT LAST_INSERT_ID() AS receipt_id;")[0][0])
            for item in item_data:
                item_tax = item["price"] * item["quantity"] * item["tax_rate"]
                backend.run_query(
                    "INSERT INTO receipt_item (receipt_id, item_id, quantity, item_price, item_tax) VALUES (%s, %s, %s, %s, %s);",
                    (receipt_id, item["item_id"], item["quantity"], item["price"], item_tax)
                )
                backend.run_query("UPDATE inventory_item SET quantity = quantity - %s WHERE item_id = %s;", (item["quantity"], item["item_id"]))
                subtotal += item["price"] * item["quantity"]
                total_tax += item_tax
            total_amount = subtotal + total_tax
            amount_due = total_amount + tip
            backend.run_query(
                "UPDATE receipt SET total_amount = %s, amount_due = %s WHERE receipt_id = %s;",
                (total_amount, amount_due, receipt_id)
            )
            backend.run_query(
                "INSERT INTO transaction (customer_email, total, tip_amount, status) VALUES (%s, %s, %s, 'Completed');",
                (customer_email, amount_due, tip)
            )
            return{
                "success": True,
                "receipt_id": receipt_id,
                "subtotal": round(subtotal, 2),
                "tax": round(total_tax, 2),
                "tip": round(tip, 2),
                "amount_due": round(amount_due, 2)
            }
        except Exception as e:
            return {"success": False, "message": str(e)}

    def rate_item(self, customer_email, item_name, rating): #Dariya
        """
        Allows a customer to rate an item (1-5 stars) and updates the item's average rating
        :param customer_email: email of customer
        :param item_name: name of the inventory item
        :param rating: integer rating from 1-5
        """
        try:
            if rating < 1 or rating > 5:
                return {"success": False, "message": "Rating must be between 1 and 5"}
            if not backend.run_query("SELECT email FROM customer WHERE email = %s;", (customer_email,)):
                return {"success": False, "message": "Customer not found"}
            # get item_id from name
            result = backend.run_query("SELECT item_id FROM inventory_item WHERE item_name = %s;", (item_name,))
            if not result:
                return {"success": False, "message": "Item not found"}
            item_id = result[0][0]
            # check if the customer already rated the item
            existing = backend.run_query(
                "SELECT rating_id FROM item_rating WHERE customer_email = %s AND item_id = %s;", (customer_email,item_id))
            if existing:
                backend.run_query("UPDATE item_rating SET rating = %s, created_at = CURRENT_TIMESTAMP WHERE rating_id = %s;",
                                  (rating, existing[0][0]))
            else:
                backend.run_query("INSERT INTO item_rating (customer_email, item_id, rating) VALUES (%s, %s, %s);",
                                  (customer_email, item_id, rating))
            # recalculate the average rating for the item
            average_result = backend.run_query("SELECT AVG(rating) FROM item_rating WHERE item_id = %s;", (item_id,))
            if average_result and average_result[0][0] is not None:
                avg_rating = float(average_result[0][0])
            else:
                avg_rating = 0.0
            backend.run_query("UPDATE inventory_item SET avg_rating = %s WHERE item_id = %s;", (avg_rating, item_id))
            return {"success": True, "message": "Rating recorded and updated successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def give_feedback(self): #Azul
        pass