import Backend.password_security as password_security # for password hashing
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
security = password_security.Security()

class Payment:
    def add_payment_method(self): # Dariya
        pass
    
    def split_payment(self, receiptID, numPeople): # Azul
        """asks for the number of people splitting and it checks to see if it's greater than zero.
        then it calculates each persons total and prints it"""        
        #checks if not zero
        if numPeople <= 0:
            return "Must be higher than zero. Try again. "

        #get total from receipt
        try:
            query = "SELECT total_amount FROM receipt WHERE receipt_id = %s;"
            result = backend.run_query(query, (receiptID,))
            total = float(result[0][0])

        except Exception as e:
            print(f"Error finding receipt {e}")

        #splits total 
        eachTotal = total/numPeople
        return eachTotal

    def apply_discounts(self): # Shalom
        pass

    def add_tips(self): # Dariya
        pass

    def add_item_to_bill(self, receiptID, item, price, quantity): # Azul
        #if item is already on bill, it updates quantity. If not it adds new item
        try:
            query = "SELECT item_id FROM inventory_item WHERE item = %s;"
            result = backend.run_query(query, (item,))
            if not result:
                print(f"Item '{item}' not found in inventory.")
                return
            item_id = result[0][0] 

            query = "SELECT quantity FROM receipt_item WHERE receipt_id = %s AND item_id = %s;"
            result = backend.run_query(query, (receiptID, item_id))
            
            #update quantity in receipt
            if result:
                quantity = result[0][0] + quantity
                query = "UPDATE receipt_item SET quantity = %s WHERE receipt_id = %s AND item_id = %s;"
                backend.run_query(query, (quantity, receiptID, item_id))
                print(f"Updated {item} quantity to {quantity} for receipt {receiptID}.")
            #create item into receipt
            else:
                query = "INSERT INTO receipt_item (receipt_id, item_id, quantity, item_price) VALUES (%s, %s, %s, %s);"
                backend.run_query(query, (receiptID, item_id, quantity, price))
                print(f"Added {quantity} x {item} to receipt {receiptID}.")

        except Exception as e:
            print(f"Error adding item to SQL: {e}")
        

    def remove_item_from_bill(self): # Shalom
        pass

    def void_transaction(self): # Dariya
        pass

    def approve_voided_transaction(self, receiptID, adminEmail, code): # Azul
        try:
            """asks for code input, then retrieves code from database and compares. After confirmation it asks to approve void and ends transaction if yes"""
            # Get for admin code
            try:
                query = "SELECT admin_code FROM user WHERE email = %s AND user_type = 'Admin';"
                result = backend.run_query(query, (adminEmail,))

            except Exception as e:
                print(f"Error find query in SQL: {e}")

            correct = str(result[0][0])

            # Compare codes
            if code != correct:
                print("Incorrect admin code. Void not approved.")
                return False

            # Confirm with user
            confirm = input("Do you approve this void? (y/n): ")
            if confirm.lower() == "n":
                print("Void not approved.")
                return False

            # Cancel transaction in database
            query = "DELETE FROM receipt WHERE receiptID = %s;"
            backend.run_query(query, (receiptID,))
            print(f"Transaction {receiptID} canceled successfully.")
            return True

        except Exception as e:
            print(f"Error approving void: {e}")
            return False

    def manage_refund(self): # Shalom
        pass