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

class Inventory:
    def add_item_to_category(self, item_ID, category):
        '''Assigns an item to a category.'''
        try:
            query = "UPDATE inventory_item SET category = %s WHERE item_id = %s"
            updated = backend.run_query(query, (category, item_ID))
            return bool(updated)
        except Exception as e:
            print(f"Error assigning item to category: {e}")
            return False
    def track_inventory(self, lowStock_limit=4): # Dariya
        """
        Retrieve inventory items and prints low stock alerts
        :param lowStock_limit: quantity at or below which a stock alert is raised
        """
        try:
            query = "SELECT item_id, item_name, quantity, price, category FROM inventory_item"
            items = backend.run_query(query,)
            if not items:
                print("No items found in the inventory.")
                return []
            print("Inventory Stock:")
            for item in items:
                alert = " LOW STOCK!!" if item['quantity'] <= lowStock_limit else ""
                print(f"ID: {item['item_id']}, Name: {item['item_name']}, "
                      f"Qty: {item['quantity']}, Price: ${item['price']}, "
                      f"Category: {item['category']}{alert}")
            return items
        except Exception as e:
            print(f"Error fetching inventory: {e}")
            return []

    def add_to_inventory(self, name, price, quantity, category): # Azul
        #check to see if item already exists
        try:
            query = "SELECT item_id FROM inventory_item WHERE item_name = %s;"
            exist = backend.run_query(query, (name,))
            if exist:
                print(f"Item '{name}' already exists in inventory.")
                return False
            
            #add to the database
            insertQuery = 'INSERT INTO inventory_item (item_name, price, quantity, category_id) VALUES (%s, %s, %s, %s)'
            backend.run_query(insertQuery, (name, price, quantity, category))
            print(f"Added successfully")
            return True

        except Exception as e:
            print(f"Error adding item to SQL: {e}")
            return False


    def update_product(self,product_name, price, quantity, category): # Shalom
        '''
        update product's price, quantity and category
        returns true or false based on successful update
        '''
        try:
            query = 'UPDATE inventory_item SET price = %s, quantity = %s, category = %s WHERE item_name = %s'

            result = backend.run_query(query, (price, quantity, category, product_name))

            if not result:
                return False
            
            if result:
                return True
            
        except Exception as e:
            print(f"An exception occoured {e}")
            return False

    def find_product(self, item_name): # Shalom
        '''
        Finds item in inventory using item name
        returns the id, price and quantity left
        '''
        
        try:
            query = "SELECT item_id, price, quantity FROM inventory_item WHERE item_name = %s"

            result = backend.run_query(query,(item_name,))

            if not result:
                return None
            
            id, price, quantity = result[0]

            return id, price, quantity
        
        except Exception as e:
            print(f"An exception occoured {e}")
            return None
        
    def add_categories(self, category_name): #Shalom
        query = "INSERT INTO category (category_name) VALUES(%s)"
        inserted = backend.run_query(query, (category_name,))
        if inserted:
            return True
        else:
            return False

    def add_item_to_category(self, item_ID, category): #Shalom

        item_query = "SELECT item_id FROM inventory_item WHERE item_id = %s"

        item_present = backend.run_query(item_query, (item_ID))

        if item_present:
            add_query = "UPDATE inventory_item SET category_id = %s WHERE item_id = %s"
            added = backend.run_query(add_query,(category, item_ID))
            if added:
                return True
            else:
                return False
        else:
            return False
        
    def delete_item(self, item_id):
        try:
            query = "DELETE FROM inventory_item WHERE item_id = %s"
            result = backend.run_query(query, (item_id,))
            return bool(result)
        except Exception as e:
            print(f"Error deleting item: {e}")
            return False
