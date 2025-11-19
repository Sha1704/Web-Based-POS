class Inventory:
    
    def track_inventory(self): # Dariya
        pass

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