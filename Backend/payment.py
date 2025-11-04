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
backend.run_query('use password_manager;')

class Payment:
    def add_payment_method(self): # Dariya
        pass
    
    def split_payment(self): # Azul
        pass

    def apply_discounts(self, discount_percent: int, total: float): # Shalom
        '''
        get discount percent and total to apply discount to as param
        return new total
        '''

        new_total = total * (1 - discount_percent / 100)
        return new_total

    def add_tips(self): # Dariya
        pass

    def add_item_to_bill(self): # Azul
        pass

    def remove_item_from_bill(self, item_to_remove_id, receipt_id): # Shalom
        '''
        run sql query to remove item form receipt item
        '''
        
        query = 'DELETE FROM receipt_item WHERE item_id = %s and receipt_id = %s'

        success = backend.run_query(query, (item_to_remove_id, receipt_id,))

        if success:
            return True
        else:
            return False

    def void_transaction(self): # Dariya
        pass

    def approve_voided_transaction(self): # Azul
        pass

    def manage_refund(self, admin_code, admin_email, total_due, refund_amount, receipt_id): # Shalom
        '''
        get admin code and total due as param
        if valid
            approve refund
                make the total due - original total due in database
            return true
        else
            don't approve refund
            return flase
        '''
        query = 'SELECT admin_code from user where email = %s'

        result = backend.run_query(query, (admin_email,))

        if not result or admin_code != result[0][0]:
            return False
        else:

            new_total_due = total_due - refund_amount
            note = 'item refunded'

            update_query = 'UPDATE receipt SET amount_due = %s, note = %s WHERE receipt_id = %s'

            updated = backend.run_query(update_query, (new_total_due, note, receipt_id,))

            if updated:
                return True
            else:
                return False
            
        