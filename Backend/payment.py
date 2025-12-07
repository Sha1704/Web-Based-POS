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

# Ensure correct database is used
backend.run_query('use web_based_pos;')

class Payment:
    """
    Handles payment processing: add payment method, split payment, apply discount, add tips, add items, remove item, 
    void transaction, approve voided transaction and manage refund.
    """
    
    def add_payment_method(self, receiptID, payment_type, amount): # Dariya 
        """
        Adds payment method to transaction linked to a receipt

        :param receiptID: ID of receipt to add payment
        :param payment_type: Type of payment like cash or card
        :param amount: Amount paid using the method
        :return: True if payment method added successfully, otherwise False
        """
        try:
            payment_query = 'INSERT INTO payment_method (receipt_id, payment_type, amount) VALUES (%s, %s, %s)'
            backend.run_query(payment_query, (receiptID, payment_type, amount))
            return True
        
        except Exception as e:
            print(f"An error occurred while adding payment method: {e}")
            return False
    
    def split_payment(self, receiptID, numPeople): # Azul
        """asks for the number of people splitting and it checks to see if it's greater than zero.
        then it calculates each persons total and prints it"""        
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

    def apply_discounts(self, discount_code: int, total: float): # Shalom
        '''
        get discount percent and total to apply discount to as param
        return new total
        '''
        query = "SELECT discount_percent FROM discount WHERE discount_code = %s"
        code = backend.run_query(query, (discount_code,))
        new_total = total * (1 - code[0] / 100)
        return new_total

    def add_tips(self, receiptID, tip_amount): # Dariya
        """
        Adds tip to existing transaction linked to a receipt

        :param receiptID: ID of receipt to add tip
        :param tip_amount: Tip amount to add
        :return: True if tip added successfully, otherwise False
        """
        try:
            tip_query = 'UPDATE transaction SET tip_amount = tip_amount + %s WHERE receipt_id = %s'
            backend.run_query(tip_query, (tip_amount, receiptID))
            return True
        
        except Exception as e:
            print(f"An error occurred while adding tip: {e}")
            return False
        
    def add_item_to_bill(self, receiptID, item_id, quantity, price):
        try:
            # Check inventory
            query = "SELECT item_id FROM inventory_item WHERE item_id = %s;"
            result = backend.run_query(query, (item_id,))
            if not result:
                print(f"Item ID '{item_id}' not found in inventory.")
                return False

            # Check if item already exists on this bill
            query = "SELECT quantity FROM receipt_item WHERE receipt_id = %s AND item_id = %s;"
            result = backend.run_query(query, (receiptID, item_id))

            if result:
                # Update quantity
                new_qty = result[0][0] + quantity
                update_query = """
                    UPDATE receipt_item 
                    SET quantity = %s 
                    WHERE receipt_id = %s AND item_id = %s;
                """
                backend.run_query(update_query, (new_qty, receiptID, item_id))
                print(f"Updated item {item_id} quantity to {new_qty} for receipt {receiptID}.")
        
            else:
                # Insert new item
                insert_query = """
                    INSERT INTO receipt_item (receipt_id, item_id, quantity, item_price)
                    VALUES (%s, %s, %s, %s);
                """
                backend.run_query(insert_query, (receiptID, item_id, quantity, price))
                print(f"Added {quantity} x item {item_id} to receipt {receiptID}.")
            update_totals_query = """
                UPDATE receipt
                SET total_amount = (
                    SELECT COALESCE(SUM(quantity * item_price), 0)
                    FROM receipt_item
                    WHERE receipt_id = %s
                ),
                amount_due = (
                    SELECT COALESCE(SUM(quantity * item_price), 0)
                    FROM receipt_item
                    WHERE receipt_id = %s
                )
                WHERE receipt_id = %s;
            """
            backend.run_query(update_totals_query, (receiptID, receiptID, receiptID))
            print(f"Updated totals for receipt {receiptID}.")

            return True

        except Exception as e:
            print(f"Error adding item to SQL: {e}")
            return False
    
    def remove_item_from_bill(self, item_line_id, receipt_id): # Shalom
        '''
        run sql query to remove item form receipt item
        '''
        
        query = 'DELETE FROM receipt_item WHERE item_line_id = %s and receipt_id = %s'

        success = backend.run_query(query, (item_line_id, receipt_id,))

        if success:
            return True
        else:
            return False

    def void_transaction(self, receiptID, admin_email, admin_code): # Dariya 
        """
        Voids a transaction by marking it as canceled
        Requires a valid admin code

        :param receiptID: ID of receipt to void
        :param admin_email: Admin email to verify
        :param admin_code: Admin code to verify
        :return: True if transaction voided successfully, otherwise False
        """ 
        try:
            admin_query = "SELECT admin_code FROM user WHERE email = %s AND user_type = 'Admin'"
            result = backend.run_query(admin_query, (admin_email,))
            if not result or admin_code != result[0][0]:
                return False
            
            
            void_query = """
                UPDATE receipt 
                SET amount_due = 0, note = 'Voided' 
                WHERE receipt_id = %s
            """
            backend.run_query(void_query, (receiptID,))

            return True
        
        except Exception as e:
            print(f"An error occurred while voiding transaction: {e}")
            return False

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

    def manage_refund(self, admin_code, admin_email, total_due, refund_amount, receipt_id):
        """
        Validates admin, applies refund, updates receipt.
        If receipt becomes fully refunded (<= 0), mark it as 'Refunded'.
        """

        # Verify admin
        query = 'SELECT admin_code FROM user WHERE email = %s'
        result = backend.run_query(query, (admin_email,))

        if not result or admin_code != result[0][0]:
            return False

        # Calculate new amount_due
        new_total_due = total_due - refund_amount
        note = 'item refunded'

        # Update amount_due
        update_query = 'UPDATE receipt SET amount_due = %s, note = %s WHERE receipt_id = %s'
        updated = backend.run_query(update_query, (new_total_due, note, receipt_id))

        if not updated:
            return False

        # If fully refunded, mark officially refunded
        if new_total_due <= 0:
            refund_mark_query = """
                UPDATE receipt
                SET amount_due = 0,
                    note = 'Refunded'
                WHERE receipt_id = %s
            """
            backend.run_query(refund_mark_query, (receipt_id,))

        return True

    def update_receipt_totals(self, receipt_id):
        """
        Recalculates subtotal, tax, and amount_due for a receipt.
        """
        try:
            # Sum all item totals
            query = """
                SELECT 
                    SUM(quantity * item_price) AS subtotal,
                    SUM(item_tax) AS tax
                FROM receipt_item
                WHERE receipt_id = %s
            """
            result = backend.run_query(query, (receipt_id,))

            subtotal = result[0][0] if result[0][0] else 0
            tax = result[0][1] if result[0][1] else 0
            total = subtotal + tax

            # Update the receipt table
            update_query = """
                UPDATE receipt
                SET total_amount = %s,
                    amount_due = %s
                WHERE receipt_id = %s
            """
            backend.run_query(update_query, (total, total, receipt_id))

            print(f"Receipt {receipt_id} updated: total={total}, due={total}")
            return True

        except Exception as e:
            print("Error in update_receipt_totals:", e)
            return False

            
        