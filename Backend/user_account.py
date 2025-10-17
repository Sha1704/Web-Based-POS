import Backend.password_security as password_security # for password hashing
import backend_sql as sql # for sql queries
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

    def create_account(self, email, password, user_type, security_question, security_answer): # Shalom
        """
        Creates a new user account and stores hashed password.

        :param password: User's password
        :param email: User's email address
        :param user_type: the user type (admin, employee or customer)
        :return: True if user created, False otherwise
        """
        try:
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
                hashed_security_answer = security.hash_data(security_answer.lower())

                backend.run_query(query, (email.lower(), hashed_password, user_type.lower(), security_question, hashed_security_answer))

                return True
        except Exception as e:
            print(f"An error occurred: {e}")

    def log_in(self, email, password, ): # Dariya

        """
        Authenticates a user by verifying the password.

        :param email: email to log in
        :param password: password to verify
        :return: Tuple (True, encryption_key) if successful, (False, None) otherwise
        """

        pass

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
                    email_query = 'SELECT email FROM user WHERE email = %s'
                    email_exists = backend.run_query(email_query, (email,))

                    if email_exists:
                        question_query = 'SELECT security_answer FROM user WHERE email = %s'
                        answer_hash = backend.run_query(question_query, (security_answer,))

                        same_answer = security.verify_hashed_data(security_answer, answer_hash)

                        if same_answer:
                            hashed_new_password = security.hash_data(new_password)

                            add_password_query = 'update user set password_hash = %s where email = %s'
                            password_replaced = backend.run_query(add_password_query, (hashed_new_password, email))

                            if password_replaced:
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                         return False
                    
                except Exception as e:
                    print(f"An error occurred: {e}")
    
    def get_security_question(self, email): # Shalom
         
        """
        Gets the security question from database.

        :param email: User's email
        :return: The security question
        """
        
        try:
           security_question_query = 'select security_question from user where email = %s'
           question = backend.run_query(security_question_query, (email,))

           return question
        
        except Exception as e:
           print(f"An error occurred: {e}")