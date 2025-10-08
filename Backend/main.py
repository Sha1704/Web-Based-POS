from backend_sql import backend_sql as sql
from account import account as acc
from dotenv import load_dotenv # you have to import dotenv (see dependencies.txt file)
import os

# Loads variables from .env in the current directory
load_dotenv()

# Load database credentials from environment
database_host = os.getenv("DB_HOST")
database_user = os.getenv("DB_USER")
database_password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")

# Create class instances for database, user management(account class).
account_class = acc()
sql_class = sql.Backend(database_host, database_user, database_password, database)


class main:

    """
    Handles user input and menu navigation.
    """

    pass