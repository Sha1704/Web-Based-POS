import mysql.connector # you have to install mysql
from mysql.connector import Error, ProgrammingError

class Backend:

    """
    Handles database connection and query execution.
    """

    def __init__(self, host, user, password, database):
        """
        Initialize the Backend class with database connection parameters.

        :param host: Database host address
        :param user: Database username
        :param password: Database password
        :param database: Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    def run_query(self, query:str, params = None): # Shalom
        """
        Executes a SQL query on the database.

        :param query: SQL query string
        :param params: Optional tuple of parameters for parameterized queries
        :return:
            - list: For SELECT queries that return rows.
            - []: For SELECT queries with no results.
            - True: For successful INSERT, UPDATE, or DELETE queries (regardless of affected rows).
            - None: If a database or programming error occurs.
        """

        data_base = None
        cursor = None

        try:
            # Connect to the database
            data_base = mysql.connector.connect(host = self.host, user = self.user, password = self.password, database = self.database)
            cursor = data_base.cursor()
            # Execute query with or without parameters
            if params:
                cursor.execute(query,params)
            else:
                cursor.execute(query)

            # Handle SELECT queries
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                if results != []:
                    # Return results if found
                    return results
                else:
                    print('No results found')
                    return []

            # Handle INSERT, UPDATE, DELETE queries
            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                data_base.commit()
                return True
                
        except ProgrammingError as pe:
            print(f'Programing error: {pe}')
            return None
        except Error as e:
            print(f'An error occured: {e}')
            return None
        finally:
            # Clean up database resources
            if cursor is not None:
                cursor.close()
            if data_base is not None and data_base.is_connected():
                data_base.close()  

    # run_insert() method
    # Zoe Steinkoenig
    # Added 12-05-2025
    def run_insert(self, query: str, params=None):
        """
        Executes an INSERT query and returns the newly generated primary key ID.

        :param query: SQL INSERT statement
        :param params: Optional tuple for parameterized queries
        :return:
            - int: last inserted row ID
            - None: if an error occurs
        """

        data_base = None
        cursor = None

        try:
            # Connect to DB
            data_base = mysql.connector.connect(
                host=self.host, 
                user=self.user, 
                password=self.password, 
                database=self.database
            )
            cursor = data_base.cursor()

            # Execute the INSERT
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Commit the transaction
            data_base.commit()

            # Get last inserted ID
            new_id = cursor.lastrowid

            return new_id

        except ProgrammingError as pe:
            print(f"Programming error: {pe}")
            return None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if data_base is not None and data_base.is_connected():
                data_base.close()
