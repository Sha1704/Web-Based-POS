import smtplib 
from data import backend_sql as sql 
from email.mime.text import MIMEText 
from dotenv import load_dotenv 
import os 

load_dotenv() 

#emails for request maintance
EMAIL_USER = os.getenv("EMAIL_USER") 
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") 
MAINTENANCE_EMAIL = os.getenv("MAINTENANCE_EMAIL") 

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
        #shows each receipt  
        try: 
            query = """ 
            SELECT  
                r.receipt_id, 
                r.created_at, 
                i.item_name, 
                ri.quantity, 
                (ri.quantity * ri.item_price) AS line_total 
            FROM receipt r 
            JOIN receipt_item ri ON r.receipt_id = ri.receipt_id 
            JOIN inventory_item i ON i.item_id = ri.item_id 
            ORDER BY r.receipt_id; 
            """ 
            sales = backend.run_query(query) 

            if not sales: 
                print("No sales found.") 
                return [] 

            print("\n========= SALES REPORT =========\n") 

            for s in sales: 
                print(f"Receipt #{s['receipt_id']} | Date: {s['created_at']} | " 
                    f"Item: {s['item_name']} | Qty: {s['quantity']} | " 
                    f"Line Total: ${s['line_total']:.2f}") 

            print("\n================================\n") 
            return sales 

        except Exception as e: 
            print(f"Error: {e}") 
            return [] 


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

    def request_maintance(self, code, message): #Azul
        ''' 
        gets admin code and message, checks to see admin code is correct, sends message through email 
        ''' 
        try: 
            #check admin code 
            admin_query = """SELECT admin_code FROM user WHERE admin_code = %s AND user_type = 'Admin'""" 
            result = backend.run_query(admin_query, (code,)) 

            if not result: 
                print("Invalid code") 
                return False 

            #send email 
            email_subject = "Maintenance Request" 
            email_body = f"""Admin Code: {code} Maintenance Issue: {message}""" 

            msg = MIMEText(email_body) 
            msg["Subject"] = email_subject 
            msg["From"] = EMAIL_USER 
            msg["To"] = MAINTENANCE_EMAIL 

            with smtplib.SMTP("smtp.gmail.com", 587) as server: 
                server.starttls() 
                server.login(EMAIL_USER, EMAIL_PASSWORD) 
                server.sendmail(EMAIL_USER, MAINTENANCE_EMAIL, msg.as_string()) 

            print("Maintenance request successful.") 
            return True 

        except Exception as e: 
            print(f"Error sending maintenance email: {e}") 
            return False 