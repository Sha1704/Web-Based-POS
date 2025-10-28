import Backend.password_security as password_security # for password hashing
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
security = password_security.Security()



class Account:
    
    """
    Handles user account management: creation, login, logout, password reset/changes.
    """

    def __init__(self, database):
           """
           Initialize the account instance with a backend database and security handler
           """
           self.database = database
           self.security = password_security.Security()
    
    def create_account(self, email, password, user_type, security_question, security_answer): # Shalom
        """
        Creates a new user account and stores hashed password.

        :param password: User's password
        :param email: User's email address
        :param user_type: the user type (admin, employee or customer)
        :return: True if user created, False otherwise
        """
        try:

            email = email.strip().lower()
            user_type = user_type.strip().lower()
            security_question = security_question.strip()
            security_answer = security_answer.strip().lower()

            # Check if email already exists
            email_query = 'SELECT email FROM user WHERE email = %s'
            email_exists = backend.run_query(email_query, (email,))

            if email_exists:
                print('The email you entered is already in use')
                return False
            else:
                # Insert new user
                query = 'INSERT INTO user (email, password_hash, user_type, security_question, security_answer) VALUES (%s, %s, %s, %s, %s);'

                hashed_password = security.hash_data(password)
                hashed_security_answer = security.hash_data(security_answer)

                backend.run_query(query, (email, hashed_password, user_type, security_question, hashed_security_answer))

                return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def log_in(self, email, password, ): # Dariya

        """
        Authenticates a user by verifying the password.

        :param email: email to log in
        :param password: password to verify
        :return: Tuple (True, encryption_key) if successful, (False, None) otherwise
        """
        # check if user exists
        user_data = self.database.run_query(email)
        if not user_data:
               print("Login failed: Email not found.")
               return False, None
        stored_hashed_password, role = user_data
        # verify password
        if self.security.verify_hashed_password(password, stored_hashed_password):
               print(f"Login successful. Role: {role}")
               # placeholder for encryption 
               encryption_key = f"key_for_{email}"
               return True, encryption_key
        else:
               print("Login failed: Incorrect password.")
               return False, None

    def log_out(self): # Azul
                """
                Terminates the current user session.

                Returns:
                - True if a session was active and was successfully terminated.
                - False if there was no active session.
                """

                pass

    def password_reset(self, email, new_password, security_answer): # Shalom
                """
                Reset the user's password to a new password.

                :param new_password: Plaintext new password provided by the user.
                :return: True when the password was successfully changed,
                False otherwise.
                """
                try:
                    email = email.strip().lower()
                    security_answer = security_answer.strip().lower()

                    question_query = 'SELECT security_answer FROM user WHERE email = %s'
                    result = backend.run_query(question_query, (email,))
                    
                    if not result:
                        return False
                    
                    answer_hash = result[0][0]
                    same_answer = security.verify_hashed_data(security_answer, answer_hash)

                    if same_answer:
                        hashed_new_password = security.hash_data(new_password)

                        add_password_query = 'update user set password_hash = %s where email = %s'
                        password_replaced = backend.run_query(add_password_query, (hashed_new_password, email))

                        return bool(password_replaced)
                    else:
                        return False
                    
                except Exception as e:
                    print(f"An error occurred: {e}")
                    return False
    
    def get_security_question(self, email): # Shalom
         
        """
        Gets the security question from database.

        :param email: User's email
        :return: The security question
        """
        
        try:
           email = email.strip().lower()
           security_question_query = 'select security_question from user where email = %s'
           question = backend.run_query(security_question_query, (email,))

           return question[0][0] if question else False
        
        except Exception as e:
           print(f"An error occurred: {e}")
           return False