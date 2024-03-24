from cryptography.fernet import Fernet

# Initialize the Fernet object with the provided key
key = b'CUUyw4rFXuLqpufCrtViUtPjL9BvB1gopW1nssEht84='
cipher_suite = Fernet(key)

# Example of encrypting a message
message = b"Sensitive information"
cipher_text = cipher_suite.encrypt(message)
print("Encrypted message:", cipher_text)

# Example of decrypting a message
plain_text = cipher_suite.decrypt(cipher_text)
print("Decrypted message:", plain_text.decode())
