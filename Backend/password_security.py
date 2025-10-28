import bcrypt

class Security:
    """
    Provides password hashing utilities.
    """
    
    def hash_data(self, password_to_hash): # Shalom
        """
        Hashes a password using bcrypt.

        :param password_to_hash: Password string to hash
        :return: Hashed password (bytes)
        """
        generated_salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password = password_to_hash.encode(), salt = generated_salt)
        return hashed_password

    def verify_hashed_data(self, user_data, hash_data): # Shalom
        """
        Verifies a data against a bcrypt hash.

        :param user_password: Plain data to check
        :param hash_password: Hashed data to verify against
        :return: True if match, False otherwise
        """
        # bcrypt expects bytes, so encode both
        if bcrypt.checkpw(password = user_data.encode(), hashed_password = hash_data.encode()): # hash_data.encode() might be an issue keep an eye on it
            return True
        else:
            return False
