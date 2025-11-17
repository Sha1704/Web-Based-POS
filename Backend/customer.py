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
    def redeem_loyalty_point(self, email: str, pointsRedeem: int, receipt_id: int): # Dariya
        """
        Redeem loyalty points to reduce receipt amount.
        Use point to cash ratio from points_redeem_settings table with default of 0.01
        """
        try:
            ratio_result = backend.run_query(
                "SELECT settingValue FROM points_redeem_setting WHERE settingName = 'point_to_cash';"
            )
            pointToCash = float(ratio_result[0][0]) if ratio_result else 0.01
            result = backend.run_query(
                "SELECT points FROM customer WHERE email=%s;",(email,)
            )
            if not result:
                return "Customer not found."
            currPoints = result[0][0]
            # check enough points
            if currPoints < pointsRedeem:
                return "Not enough points."
            # receipt info
            receipt = backend.run_query(
                "SELECT total_amount, amount_due FROM receipt WHERE receipt_id=%s;",(receipt_id,)
            )
            if not receipt:
                return "Receipt not found."
            total_amount, amount_due = receipt[0]
            # calculate discount using ratio
            discount = pointsRedeem * pointToCash
            if discount > amount_due:
                discount = amount_due
            new_amount_due = amount_due - discount
            # update receipt
            backend.run_query(
                "UPDATE receipt SET amount_due=%s WHERE receipt_id=%s;",(new_amount_due, receipt_id) 
            )
            # deduct customer points
            newPoints = currPoints - pointsRedeem
            backend.run_query(
                "UPDATE customer SET points=%s WHERE email=%s;", (newPoints, email)
            )
            return f"Redeemed Successfully! New balance: {newPoints} points. Discount applied: ${discount:.2f}"
        except Exception as e:
            return f"System error occurred: {e}"