from passlib.context import CryptContext


class Security:
    __cripto = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def __get_cripto(cls) -> CryptContext:
        return cls.__cripto

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Function to verify the password is correct
        """
        return Security.__get_cripto().verify(password, hashed_password)

    @staticmethod
    def create_hash_password(password: str) -> str:
        """
        Function to create a hash password
        """

        return Security.__get_cripto().hash(password)
