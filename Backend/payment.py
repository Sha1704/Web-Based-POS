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
    
    def split_payment(self, total): # Azul
        """asks for the number of people splitting and it checks to see if it's greater than zero.
        then it calculates each persons total and prints it"""
        split = int(input("How many people are splitting? "))
        
        #checks if not zero
        while split <= 0:
            split = int(input("Must be higher than zero. Try again. "))

        #splits total 
        eachTotal = total/split
        print(eachTotal)

        #input data into database
        try:
            query = 'INSERT INTO payment (total, split_count) VALUES (%s, %s, %s);'
            backend.run_query(query, (total, split))
        except Exception as e:
            print(f"Error recording split payment: {e}")

    def apply_discounts(self): # Shalom
        pass

    def add_tips(self): # Dariya
        pass

    def add_item_to_bill(self, bill, name, price, quantity): # Azul
        #if item is already on bill, it updates quantity. If not it adds new item
        if name in bill:
            bill[name]["quantity"] += quantity
        else:
            bill[name] = {"price": price, "quantity": quantity}
        
        #add to database
        try:
            query = 'INSERT INTO payment_item (item_name, price, quantity) VALUES (%s, %s, %s);'
            backend.run_query(query, (name, price, quantity))
            
        except Exception as e:
            print(f"Error adding item to SQL: {e}")

    def remove_item_from_bill(self): # Shalom
        pass

    def void_transaction(self): # Dariya
        pass

    def approve_voided_transaction(self, bill): # Azul
        try:
            """asks for code input, then retrieves code from database and compares. After confirmation it asks to approve void and ends transaction if yes"""
            # Ask for admin code
            entered_code = input("Enter admin code: ")

            # Retrieve admin code from database
            query = "SELECT admin_code FROM admin LIMIT 1;"  # assuming you have an admin table
            result = backend.run_query(query)

            if not result:
                print("No admin code found in database.")
                return False

            correct_code = str(result[0][0]) #get code from database and converts it to string

            # Compare codes
            if entered_code != correct_code:
                print("Incorrect admin code. Void not approved.")
                return False

            # Confirm with user
            confirm = input("Do you approve this void? (y/n): ")
            if confirm.lower() == "n":
                print("Void not approved.")
                return False

            # Cancel transaction in database
            cancel_query = "DELETE FROM payment WHERE payment_id = %s;"
            backend.run_query(cancel_query, (bill))
            print(f"Transaction {bill} canceled successfully.")
            return True

        except Exception as e:
            print(f"Error approving void: {e}")
            return False

    def manage_refund(self): # Shalom
        pass