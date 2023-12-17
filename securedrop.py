import os
import json
from contact import Contact
from cryptography.fernet import Fernet
from socket import socket
import time

class SecureDrop:

    def __init__(self, client_socket: socket, user_id="Guest"):
        self.__user_id = user_id
        self.__contacts = []
        self.__contact_info = "contacts.json"
        self.__socket = client_socket

    def main_loop(self):
        while True:
            command = input("secure_drop> ")
            if command.lower() == "help":
                self.help_command()
            elif command.lower() == "add":
                self.add_command()
            elif command.lower() == "list":
                self.list_command()
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

        filename = os.path.join(os.getcwd(), email_address)
        os.makedirs(filename, exist_ok=True)
        filename = os.path.join(filename, "name.bin")
        generate_key(filename)
        encrypted_name = encrypt_text(full_name, filename)

        filename = os.path.join(os.getcwd(), self.__contact_info)

        try:
            with open(self.__contact_info, 'r') as file:
                data = json.load(file)
        except FileNotFoundError or ValueError:
            data = []

        contacts_data = [{'UserID': email_address, 'Data': encrypted_name}]
        data.extend(contacts_data)
        updated_data = json.dumps(data, indent=2)
        with open(filename, 'w') as file:
            file.write(updated_data)

    def list_command(self):

        try:
            with open(self.__contact_info, 'r') as file:
                contacts = json.load(file)
        except FileNotFoundError or ValueError:
            contacts = []

        data = {'command': 'list_contacts', 'data': self.__user_id}
        received_data = send_data(self.__socket, data)
        # print(received_data)
        # check user has the added the contact
        # check contact has reciprocated
        # check contact is online
        # Create a client socket
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # # Connect to the server
        # server_address = ('localhost', 12345)
        # client_socket.connect(server_address)
        # # Receive data from the server
        # data = client_socket.recv(1024)
        # print('Received:', data.decode('utf-8'))
        # # Check our contacts.json
        # # Close the connection
        # client_socket.close()


def has_added_contact(user_contacts, contact_id):
    return contact_id in user_contacts


def has_reciprocated(user_contacts, contact_id):
    return user_contacts.get(contact_id, {}).get('reciprocated', False)


def is_contact_online(online_contacts, contact_id):
    return contact_id in online_contacts


def generate_key(key_file_name):
    # Generates a key and saves it to a file
    key = Fernet.generate_key()
    with open(key_file_name, "wb") as key_file:
        key_file.write(key)


def encrypt_text(text, key_file_name, ):
    # Reading the key from the key file
    with open(key_file_name, "rb") as key_file:
        key = key_file.read()

    # Generating the key using the key read in
    cipher_suite = Fernet(key)

    with open(key_file_name, "wb") as key_file:
        key_file.write(key)

    # Encrypting text
    encrypted_text = cipher_suite.encrypt(text.encode()).decode()
    return encrypted_text


def receive_data(client_socket):
    data = client_socket.recv(1024)

    # Check if data is not empty
    if not data:
        print("Error: Empty data received.")
        return None

    try:
        # Try to decode the received data as JSON
        decoded_data = json.loads(data.decode())
        return decoded_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

def send_data(client_socket, data):
    # Send data to the server
    client_socket.sendall(json.dumps(data).encode())

    # Receive the response from the server
    response_data = receive_data(client_socket)
    if response_data:
        print(f"Server response: {response_data}")
    return response_data

def decrypt_text(key_file_name, encrypted_text):
    # Reading the key from the key file
    with open(key_file_name, "rb") as key_file:
        key = key_file.read()

    # Generating the key using the key read in
    cipher_suite = Fernet(key)

    # Decrypting text
    try:
        decrypted_text = cipher_suite.decrypt(encrypted_text.encode()).decode()
        return decrypted_text
    except Exception as e:
        print(f"Error decrypting text: {e}")
        return None
