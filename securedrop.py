import os
import json

from contact import Contact
from cryptography.fernet import Fernet
from socket import socket


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
            elif command.lower() == "send":
                self.send_command()
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
        self.generate_key(filename)
        encrypted_name = self.encrypt_text(full_name, filename)

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
        print("Contact Added.")

    def list_command(self):

        try:
            with open(self.__contact_info, 'r') as file:
                contacts = json.load(file)
        except FileNotFoundError or ValueError:
            contacts = []

        data = {'command': 'list_contacts', 'data': self.__user_id}
        received_data = send_data(self.__socket, data)
        if len(received_data['contacts']) > 0:
            print("The following contacts are online:")
            for contact_id in received_data['contacts']:
                filename = os.path.join(os.getcwd(), contact_id, "name.bin")
                for contact in contacts:
                    if contact['UserID'] == contact_id:
                        print(f"* {self.decrypt_text(filename, contact['Data'])} <{contact_id}>")
        else:
            print("No contacts are online at this time!")
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

    def send_command(self):
        file_path = input("Enter path to the file: ")
        contact_email = input("Enter the email of the contact to send to: ")

        # Ensure the file exists
        if not os.path.isfile(file_path):
            print("File does not exist.")
            return

        # Load contacts from the contacts.json file
        try:
            with open('contacts.json', 'r') as file:
                contacts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error loading contacts. Please make sure contacts.json exists and is valid.")
            return

        # Check if the contact exists in the contacts list
        contact_exists = any(contact['UserID'].lower() == contact_email for contact in contacts)
        if not contact_exists:
            print("Contact not found. Please check the email address.")
            return

        # Get the key for encryption from the contact's key file
        key_file_name = os.path.join(os.getcwd(), contact_email, "name.bin")
        with open(key_file_name, "rb") as key_file:
            key = key_file.read()

        # Generating the key using the key read in
        cipher_suite = Fernet(key)

        # Open the file and read in chunks
        with open(file_path, 'rb') as file:
            chunk_size = 1024  # 1MB chunk size
            sequence_number = 0
            while True:
                print("Reading....")
                chunk = file.read(chunk_size)
                if not chunk:
                    break  # End of file

                encrypted_chunk = cipher_suite.encrypt(chunk)  # Encrypt the chunk

                # Prepare the data to be sent
                data = {
                    'command': 'send_chunk',
                    'sequence': sequence_number,
                    'data': encrypted_chunk.decode('utf-8'),  # JSON must be in text form
                    'file_name': os.path.basename(file_path),
                    'contact_email': contact_email
                }

                # Send the chunk to the server
                print(f"Data: {data}")
                response = send_data(self.__socket, data)

                # Wait for the server to acknowledge receipt
                if not response or response.get('status') != 'ok':
                    print("Failed to send chunk or server response was not okay.")
                    return
                else:
                    print(f"Getting a response with sequence number {sequence_number}")


                sequence_number += 1  # Increment the sequence number for each chunk

        # Send a message indicating the transfer is complete
        send_data(self.__socket,
                  {'command': 'end_transfer', 'file_name': os.path.basename(file_path), 'contact_email': contact_email})
        print("File transfer complete.")

    @staticmethod
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

    @staticmethod
    def decrypt_text_inplace(encrypted_text):
        # Reading the key from the key file
        key = Fernet.generate_key()
        # Generating the key using the key read in
        cipher_suite = Fernet(key)

        # Decrypting text
        try:
            decrypted_text = cipher_suite.decrypt(encrypted_text.encode()).decode()
            return decrypted_text
        except Exception as e:
            print(f"Error decrypting text: {e}")
            return None

    @staticmethod
    def encrypt_text(text, key_file_name="none"):
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

    @staticmethod
    def encrypt_text_inplace(text):
        # Reading the key from the key file
        key = Fernet.generate_key()

        # Generating the key using the key read in
        cipher_suite = Fernet(key)

        # Encrypting text
        encrypted_text = cipher_suite.encrypt(text.encode()).decode()
        return encrypted_text

    @staticmethod
    def generate_key(key_file_name):
        # Generates a key and saves it to a file
        key = Fernet.generate_key()
        with open(key_file_name, "wb") as key_file:
            key_file.write(key)


def has_added_contact(user_contacts, contact_id):
    return contact_id in user_contacts


def has_reciprocated(user_contacts, contact_id):
    return user_contacts.get(contact_id, {}).get('reciprocated', False)


def is_contact_online(online_contacts, contact_id):
    return contact_id in online_contacts


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
    # if response_data:
    #     print(f"Server response: {response_data}")
    return response_data