from typing import Dict, Any

import userReg
import userLogin
import os
import json
from contact import Contact
import hashlib
from cryptography.fernet import Fernet


class SecureDrop:

    def __init__(self, user_id="Guest"):
        self.__user_id = user_id
        self.__contacts = []
        self.__contact_info = "contacts.json"

    def main_loop(self):
        while True:
            command = input("secure_drop> ")
            if command.lower() == "help":
                self.help_command()
            elif command.lower() == "add":
                self.add_command()
            elif command.lower() == "exit":
                break
            else:
                print("Not a valid command, try one of the following: ")
                self.help_command()

    @staticmethod
    def help_command():
        print('''    \"add\" -> Add a new contact
        \"list\" -> List all online contacts
        \"send\" -> Transfer file to contact
        \"exit\" -> Exit SecureDrop''')

    def add_command(self):
        full_name = input("Enter Full Name: ").title()
        email_address = input("Enter Email Address: ").lower()

        self.__contacts.append(Contact(email_address, full_name))

        encrypted_email_address = encrypt_text(email_address, "userid.bin")
        encrypted_name = encrypt_text(full_name, "name.bin")
        filename = os.path.join(os.getcwd(), encrypted_email_address, self.__contact_info)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'a') as file:
            contacts_data = {'UserID': encrypted_email_address, 'Data': encrypted_name}
            json.dump(contacts_data, file)


def encrypt_text(text: str, key_file_name, salt='somesalt'):
    """

    :type key_file_name: str
    """
    # Password Salting: Adding salt to the password before hashing password using SHA-256

    with open("salt.txt", "w") as salt_file:
        salt_file.write(salt)

    salted_text = hashlib.sha256((text + salt).encode()).hexdigest()

    # Password Encryption: Encrypting and decrypting password using Fernet symmetric encryption
    key = Fernet.generate_key()

    with open(key_file_name, "wb") as key_file:
        key_file.write(key)

    cipher_suite = Fernet(key)

    # Encrypting password
    return cipher_suite.encrypt(salted_text.encode()).decode()


def decrypt_text(key_file_name):
    # Password Salting: Adding salt to the password
    with open("salt.txt", "r") as salt_file:
        salt = salt_file.read()
    # password + salt for added security
    # salted_password = text + salt

    # reading the key from the key file
    with open(key_file_name, "rb") as key_file:
        key = key_file.read()
    # reading the encrypted password from password file
    # with open("password_file.bin", "rb") as password_to_match:
    #     pass_match = password_to_match.read()

    # generating the key using the key read in
    cipher_suite = Fernet(key)
    # Decrypting password
    decrypted_text = cipher_suite.decrypt(key).decode()
    return decrypted_text


def main():
    # Check if needs to register or login
    my_secure_drop = SecureDrop()
    my_secure_drop.main_loop()


if __name__ == '__main__':
    main()
