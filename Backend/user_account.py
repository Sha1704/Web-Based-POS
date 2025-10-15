import Backend.password_security as password_security # for password hashing

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
    
    def create_account(self, email, password): # Shalom
        """
        Creates a new user account and stores hashed password.

        :param password: User's master password
        :param email: User's email address
        :return: True if user created, False otherwise
        """

        pass

    def log_in(self, email, password): # Dariya

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

    def password_reset(self, new_password): # Shalom
                """
                Reset the user's password to a new password.

                :param new_password: Plaintext new password provided by the user.
                :return: True when the password was successfully changed,
                False otherwise.
                """

                pass