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

class Payment:
    """
    Handles payment processing: add payment method, split payment, apply discount, add tips, add items, remove item, 
    void transaction, approve voided transaction and manage refund.
    """
    
    def add_payment_method(self, transaction_id, payment_type, amount): # Dariya
        """
        Adds payment method to transaction.

        :param transaction_id: ID of transaction to add payment
        :param payment_type: Type of payment like cash or card
        :param amount: Amount paid using the method
        :return: True if payment method added successfully, otherwise False
        """
        try:
            payment_query = 'INSERT INTO payment_method (transaction_id, payment_type, amount) VALUES (%s, %s, %s)'
            backend.run_query(payment_query, (transaction_id, payment_type, amount))
            print(f"Payment method {payment_type} of amount {amount} added to transaction {transaction_id}.")
            return True
        
        except Exception as e:
            print(f"An error occurred while adding payment method: {e}")
            return False
    
    def split_payment(self): # Azul
        pass

    def apply_discounts(self): # Shalom
        pass

    def add_tips(self, transaction_id, tip_amount): # Dariya
        """
        Adds tip to existing transaction.

        :param transaction_id: ID of transaction to add tip
        :param tip_amount: Tip amount to add
        :return: True if tip added successfully, otherwise False
        """
        try:
            tip_query = 'UPDATE transaction SET tip_amount = tip_amount + %s WHERE transaction_id = %s'
            backend.run_query(tip_query, (tip_amount, transaction_id))
            print(f"Tip of amount {tip_amount} added to transaction {transaction_id}.")
            return True
        
        except Exception as e:
            print(f"An error occurred while adding tip: {e}")
            return False

    def add_item_to_bill(self): # Azul
        pass

    def remove_item_from_bill(self): # Shalom
        pass

    def void_transaction(self, transaction_id): # Dariya
        """
        Voids a transaction by marking it as canceled

        :param transaction_id: ID of transaction to void
        :return: True if transaction voided successfully, otherwise False
        """ 
        try:
            void_query = "Update transaction SET status = 'Voided' WHERE transaction_id = %s"
            backend.run_query(void_query, (transaction_id,))
            print(f"Transaction {transaction_id} has been voided.")
            return True
        
        except Exception as e:
            print(f"An error occurred while voiding transaction: {e}")
            return False

    def approve_voided_transaction(self): # Azul
        pass

    def manage_refund(self): # Shalom
        pass