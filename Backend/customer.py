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
    
    # def order_ahead(self, item_name, quantity, pickup_time, customer_email = "orderAhead@email.com"):
    def order_ahead(self, item_name, quantity, pickup_time, customer_email):
        """
        Allows a customer to order an item ahead for pickup.
        Stores the order in the receipt and receipt_item tables.
        """
        try:
            # Check if customer exists
            customer = backend.run_query("SELECT email FROM customer WHERE email = %s;", (customer_email,))
            if not customer:
                return {"success": False, "message": "Customer not found"}

            # Check if item exists and has enough quantity
            item = backend.run_query("SELECT item_id, price, quantity FROM inventory_item WHERE item_name = %s;", (item_name,))
            if not item:
                return {"success": False, "message": "Item not found"}
            item_id, price, available_qty = item[0]
            if available_qty < quantity:
                return {"success": False, "message": "Not enough quantity available"}

            # Create a new receipt
            total_amount = price * quantity
            receipt_query = """
                INSERT INTO receipt (customer_email, total_amount, amount_due, note)
                VALUES (%s, %s, %s, %s)
            """
            backend.run_query(receipt_query, (customer_email, total_amount, total_amount, f"Pickup time: {pickup_time}"))

            # Get the newly created receipt_id
            receipt_id = backend.run_query("SELECT LAST_INSERT_ID();")[0][0]
            # Insert into receipt_item
            receipt_item_query = """
                INSERT INTO receipt_item (receipt_id, item_id, quantity, item_price)
                VALUES (%s, %s, %s, %s)
            """
            backend.run_query(receipt_item_query, (receipt_id, item_id, quantity, price))

            # Deduct quantity from inventory
            update_qty_query = "UPDATE inventory_item SET quantity = quantity - %s WHERE item_id = %s"
            backend.run_query(update_qty_query, (quantity, item_id))

            return {"success": True, "message": "Order placed successfully", "pickup_time": pickup_time}
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

    def give_feedback(self, customer_email, feedback):
        """
        Stores customer feedback in the database.
        """
        try:
            if not feedback:
                return {"success": False, "message": "Feedback cannot be empty."}
            query = "INSERT INTO customer_feedback (customer_email, message) VALUES (%s, %s)"
            backend.run_query(query, (customer_email, feedback))
            return {"success": True, "message": "Feedback submitted successfully."}
        except Exception as e:
            return {"success": False, "message": str(e)}