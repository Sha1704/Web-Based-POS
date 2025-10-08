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
    
    def run_query(self, query:str): # Shalom
        pass