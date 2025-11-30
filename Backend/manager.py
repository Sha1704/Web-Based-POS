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

class Manager:

    def view_sales_report(self): #Azul
        pass

    def print_reciept(self, receipt_id): #Dariya
        """
        Prints the details of a receipt, including customer, items and totals
        "param receipt_id: ID of the receipt to print
        """
        try:
            receipt = backend.run_query(
                "SELECT customer_email, total_amount, amount_due, created_at, note "
                "FROM receipt WHERE receipt_id = %s;", (receipt_id,))
            if not receipt:
                print(f"No receipt found with ID {receipt_id}")
                return
            receipt = receipt[0]
            print(f"\nReceipt ID: {receipt_id}")
            print(f"Customer: {receipt['customer_email'] or 'Guest'}")
            print(f"Created At: {receipt['created_at']}")
            if receipt.get('note'):
                print(f"Note: {receipt['note']}")
            print("\nItems:")
            # get all items for this receipt
            items = backend.run_query("SELECT item_id, quantity, item_price, item_tax FROM receipt_item WHERE receipt_id = %s;", (receipt_id,))
            if not items:
                print("No items found in this receipt.")
                return
            for item in items:
                # each item name
                result = backend.run_query("SELECT item_name FROM inventory_item WHERE item_id = %s;", (item['item_id'],))
                if result:
                    item_name = result[0]['item_name']
                else:
                    item_name = "Unknown"
                subtotal = item['item_price'] * item['quantity']
                total_item_price = subtotal + item['item_tax']
                print(f"- {item_name} x {item['quantity']}: ${total_item_price:.2f} "
                      f"(Price: ${item['item_price']}, Tax: ${item['item_tax']})")
            # print totals
            print(f"\nTotal Amount: ${receipt['total_amount']:.2f}")
            print(f"Amount Due: ${receipt['amount_due']:.2f}\n")
        except Exception as e:
            print(f"Error printing receipt: {e}")

    def request_maintance(self): #Azul
        '''
        send maintance request to an email
        '''
        pass