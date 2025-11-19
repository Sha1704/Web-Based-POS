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
            insertQuery = 'INSERT INTO inventory_item (item_name, price, quantity, category) VALUES (%s, %s, %s, %s)'
            backend.run_query(insertQuery, (name, price, quantity, category))
            print(f"Added successfully")
            return True

        except Exception as e:
            print(f"Error adding item to SQL: {e}")
            return False


    def update_product_count(self): # Shalom
        pass

    def find_product(self): # Shalom
        pass