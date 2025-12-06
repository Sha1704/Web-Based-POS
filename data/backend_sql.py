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
        self.data_base = None
        self.cursor = None
    
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

        try:
            # Connect to the database
            self.data_base = mysql.connector.connect(host = self.host, user = self.user, password = self.password, database = self.database)
            self.cursor = self.data_base.cursor()
            # Execute query with or without parameters
            if params:
                self.cursor.execute(query,params)
            else:
                self.cursor.execute(query)

            # Handle SELECT queries
            if query.strip().upper().startswith("SELECT"):
                results = self.cursor.fetchall()
                if results != []:
                    # Return results if found
                    return results
                else:
                    print('No results found')
                    return []

            # Handle INSERT, UPDATE, DELETE queries
            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                self.data_base.commit()
                return True
                
        except ProgrammingError as pe:
            print(f'Programing error: {pe}')
            return None
        except Error as e:
            print(f'An error occured: {e}')
            return None

    def close_connection(self):
        """
        Closes the database connection and cursor if they exist.
        """
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.data_base is not None and self.data_base.is_connected():
            self.data_base.close()
            self.data_base = None