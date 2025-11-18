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
 