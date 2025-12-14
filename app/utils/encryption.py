"""Encryption service and custom SQLAlchemy type for securing sensitive data."""

from cryptography.fernet import Fernet
from sqlalchemy import Text
from sqlalchemy.types import TypeDecorator

from app.config import settings


class EncryptionService:
    """Handles symmetric encryption and decryption of strings using Fernet."""

    def __init__(self, key: str):
        try:
            self.fernet = Fernet(key.encode())
        except Exception as e:
            raise ValueError(f"Invalid Fernet encryption key provided: {e}") from e

    def encrypt(self, data: str | None) -> str | None:
        """Encrypts a plaintext string."""
        if data is None:
            return None
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str | None) -> str | None:
        """Decrypts an encrypted string.

        Raises:
            InvalidToken: If the encrypted data is corrupted or the wrong key is used.
        """
        if encrypted_data is None:
            return None
        return self.fernet.decrypt(encrypted_data.encode()).decode()


class EncryptedType(TypeDecorator):
    """
    A SQLAlchemy TypeDecorator that provides transparent encryption for a Text column.

    - Data is encrypted when writing to the database (process_bind_param).
    - Data is decrypted when reading from the database (process_result_value).
    """

    impl = Text
    cache_ok = True
    encryption_service = EncryptionService(settings.encryption_key)

    def process_bind_param(self, value, dialect):
        """Encrypt the value before saving it to the database."""
        if value is not None:
            return self.encryption_service.encrypt(value)
        return value

    def process_result_value(self, value, dialect):
        """Decrypt the value after retrieving it from the database."""
        if value is not None:
            # InvalidToken will propagate if decryption fails
            return self.encryption_service.decrypt(value)
        return value
