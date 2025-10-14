import bcrypt

class Security:
    """
    Provides password hashing utilities.
    """
    
    def hash_password(self, password_to_hash): # Shalom
        """
        Hashes a password using bcrypt.

        :param password_to_hash: Password string to hash
        :return: Hashed password (bytes)
        """
        generated_salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password = password_to_hash.encode(), salt = generated_salt)
        return hashed_password

    def verify_hashed_password(self, user_password, hash_password): # Shalom
        """
        Verifies a password against a bcrypt hash.

        :param user_password: Plain password to check
        :param hash_password: Hashed password to verify against
        :return: True if match, False otherwise
        """
        # bcrypt expects bytes, so encode both
        if bcrypt.checkpw(password = user_password.encode(), hashed_password = hash_password.encode()):
            return True
        else:
            return False
