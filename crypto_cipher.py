from Crypto.Cipher import AES
from hashlib import sha256
import base64
import os

class URLSafeEncryptor:
    def __init__(self, password: str = None):
        """
        Инициализация шифровальщика.
        :param password: пароль для генерации ключа (если None, ключ генерируется случайно)
        """
        if password:
            # Генерируем 16-байтный ключ из пароля
            self.key = sha256(password.encode()).digest()[:16]
        else:
            # Генерируем случайный ключ
            self.key = os.urandom(16)

    def encrypt(self, message: str) -> str:
        """
        Шифрует сообщение для использования в URL.
        :param message: строка для шифрования
        :return: зашифрованное сообщение (URL-safe)
        """
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode())
        # Кодируем nonce + ciphertext + tag в URL-safe Base64
        return base64.urlsafe_b64encode(cipher.nonce + ciphertext + tag).decode('utf-8')

    def decrypt(self, encrypted_message: str) -> str:
        """
        Расшифровывает сообщение из URL.
        :param encrypted_message: зашифрованное сообщение
        :return: расшифрованное сообщение
        """
        data = base64.urlsafe_b64decode(encrypted_message)
        nonce, ciphertext, tag = data[:16], data[16:-16], data[-16:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
