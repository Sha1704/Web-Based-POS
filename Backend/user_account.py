import Backend.password_security as password_security # for password hashing

class Account:
    
    """
    Handles user account management: creation, login, logout, password reset/changes.
    """

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

        pass

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