class CryptoPlugin:
    def encrypt_data(self, data):
        return f"Encrypted({data})"
    def decrypt_data(self, data):
        return data.replace("Encrypted(", "").replace(")", "")
