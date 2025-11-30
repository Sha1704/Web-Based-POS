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

    def print_reciept(self): #Dariya
        pass

    def request_maintance(self): #Azul
        ''' 
        gets admin code and message, checks to see admin code is correct, sends message through email 
        ''' 
        try: 
            admin_code = input("Code: ") 
            message = input("Issue: ") 

            #check admin code 
            admin_query = """SELECT admin_code FROM user WHERE admin_code = %s AND user_type = 'Admin'""" 
            result = backend.run_query(admin_query, (admin_code,)) 

            if not result: 
                print("Invalid code") 
                return False 

            #send email 
            email_subject = "Maintenance Request" 
            email_body = f"""Admin Code: {admin_code} Maintenance Issue: {message}""" 

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
