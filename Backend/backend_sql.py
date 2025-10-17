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
        :return: Query result or True/False for success/failure
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
                    return False

            # Handle INSERT, UPDATE, DELETE queries
            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                data_base.commit()
                # Return True if rows affected, else False
                if cursor.rowcount == 0:
                    return False
                else:
                    return True
                
        except ProgrammingError as pe:
            print(f'Programing error: {pe}')
            return False
        except Error as e:
            print(f'An error occured: {e}')
            return False
        finally:
            # Clean up database resources
            if cursor is not None:
                cursor.close()
            if data_base is not None and data_base.is_connected():
                data_base.close()