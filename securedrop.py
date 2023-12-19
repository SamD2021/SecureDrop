import os
import json
import random
import threading
from contact import Contact
from cryptography.fernet import Fernet
from socket import socket
import time
import keyGen
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding



class SecureDrop:

    def __init__(self, client_socket: socket, user_id="Guest"):
        self.private_key: rsa.RSAPrivateKey = None
        self.__user_id = user_id
        self.__contacts = []
        self.__contact_info = "contacts.json"
        self.__socket = client_socket
        self.__recipient_key = ""
        self.__file_being_sent = []
        # Add a flag to control the notification thread
        self.notification_thread_flag = threading.Event()
        self.notification_thread_flag.set()  # Initially, the thread is allowed to run

        # Create a thread for handling notifications
        self.notification_thread = threading.Thread(target=self.notification_handler)

    def notification_handler(self):
        while self.notification_thread_flag.is_set():
            # Implement logic to check for notifications from the server
            # You might use the receive_data function or another mechanism
            self.receive_file_transfer_requests()

            # Example: Check for notifications every 5 seconds
            time.sleep(5)

    def stop_notification_thread(self):
        # Set the flag to stop the notification thread
        self.notification_thread_flag.clear()

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
                self.stop_notification_thread()  # Stop the notification thread before exiting
                break
            elif command.lower() == "receive":
                self.notification_thread.start()
                self.receive_file_transfer_requests()
            else:
                print("Not a valid command, try one of the following: ")
                self.help_command()

    @staticmethod
    def help_command():
        print('''    \"add\" -> Add a new contact
        \"list\" -> List all online contacts
        \"send\" -> Transfer file to contact
        \"recieve\" -> recieve file from contact
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

        contact_len = received_data['contacts']
        if len(contact_len) > 0:
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

    # def send_command(self):
    #     file_path = input("Enter path to the file: ")
    #     contact_email = input("Enter the email of the contact to send to: ")
    #     status, public_key_str = self.send_file_transfer_request(contact_email, file_path)
    #
    #     if status == 'approved':
    #
    #         # Ensure the file exists
    #         if not os.path.isfile(file_path):
    #             print("File does not exist.")
    #             return
    #
    #         # Load contacts from the contacts.json file
    #         try:
    #             with open('contacts.json', 'r') as file:
    #                 contacts = json.load(file)
    #         except (FileNotFoundError, json.JSONDecodeError):
    #             print("Error loading contacts. Please make sure contacts.json exists and is valid.")
    #             return
    #
    #         # Check if the contact exists in the contacts list
    #         contact_exists = any(contact['UserID'].lower() == contact_email for contact in contacts)
    #         if not contact_exists:
    #             print("Contact not found. Please check the email address.")
    #             return
    #
    #         # Get the key for encryption from the contact's key file
    #         # key_file_name = os.path.join(os.getcwd(), contact_email, "name.bin")
    #         # with open(key_file_name, "rb") as key_file:
    #         #     key = key_file.read()
    #
    #
    #         # Generating the key using the key read in
    #
    #         # Open the file and read in chunks
    #         with open(file_path, 'rb') as file:
    #             chunk_size = 1024  # 1MB chunk size
    #             sequence_number = random.randint(0, 1000000)  # Random seed for the sequence_number
    #             while True:
    #                 print("Reading....")
    #                 chunk = file.read(chunk_size)
    #                 if not chunk:
    #                     break  # End of file
    #
    #                 encrypted_chunk = cipher_suite.encrypt(chunk)  # Encrypt the chunk
    #
    #                 # Prepare the data to be sent
    #                 data = {
    #                     'command': 'send_chunk',
    #                     'sequence': sequence_number,
    #                     'data': encrypted_chunk.decode('utf-8'),  # JSON must be in text form
    #                     'file_name': os.path.basename(file_path),
    #                     'contact_email': contact_email
    #                 }
    #
    #                 # Send the chunk to the server
    #                 print(f"Data: {data}")
    #                 response = send_data(self.__socket, data)
    #
    #                 # Wait for the server to acknowledge receipt
    #                 if not response or response.get('status') != 'ok':
    #                     print("Failed to send chunk or server response was not okay.")
    #                     return
    #                 else:
    #                     print(f"Getting a response with sequence number {sequence_number}")
    #
    #                 sequence_number += 1  # Increment the sequence number for each chunk
    #
    #         # Send a message indicating the transfer is complete
    #         response = send_data(self.__socket,
    #                              {'command': 'end_transfer', 'file_name': os.path.basename(file_path),
    #                               'contact_email': contact_email, 'sequence': sequence_number})
    #         print(f"{response}")
    #     else:
    #         print("User rejected the file transfer request")
    def send_command(self):
        file_path = input("Enter path to the file: ")
        contact_email = input("Enter the email of the contact to send to: ")

        # Send file transfer request and get the status and public key
        status, public_key_str = self.send_file_transfer_request(contact_email, file_path)

        if status == 'approved':
            # Ensure the file exists
            if not os.path.isfile(file_path):
                print("File does not exist.")
                return

            # Convert the base64-encoded public key to bytes
            recipient_public_key_bytes = base64.b64decode(public_key_str.encode('utf-8'))

            # Load the recipient's public key
            recipient_public_key = serialization.load_pem_public_key(
                recipient_public_key_bytes,
                backend=default_backend()
            )

            # Open the file and read in chunks
            with open(file_path, 'rb') as file:
                chunk_size = 1024  # 1MB chunk size
                sequence_number = random.randint(0, 1000000)  # Random seed for the sequence_number
                while True:
                    chunk = file.read(chunk_size)
                    print(f"Chunk:{chunk} in send_chunk")
                    if not chunk:
                        break  # End of file

                    # Encrypt the chunk with the recipient's public key
                    encrypted_chunk = recipient_public_key.encrypt(
                        chunk,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
                    sequence_number += 1  # Increment the sequence number for each chunk
                    # Prepare the data to be sent
                    data = {
                        'command': 'send_chunk',
                        'sequence': sequence_number,
                        'data': base64.b64encode(encrypted_chunk).decode('utf-8'),  # JSON must be in text form
                        'file_name': os.path.basename(file_path),
                        'contact_email': contact_email
                    }

                    print(f"Sent to server:{data}")
                    # Send the chunk to the server
                    self.__socket.sendall(json.dumps(data).encode())
                    time.sleep(5)
                    response = receive_data(self.__socket)

                    print(f"Received from server:{response}")
                    # Wait for the server to acknowledge receipt
                    if not response or response.get('status') != 'ok':
                        print("Failed to send chunk or server response was not okay.")
                        return
                    else:
                        print(f"Getting a response with sequence number {sequence_number}")



            print("Sending End_transfer")
            # Send a message indicating the transfer is complete
            response = send_data(self.__socket,
                                 {'command': 'end_transfer', 'file_name': os.path.basename(file_path),
                                  'contact_email': contact_email, 'sequence': sequence_number})
            print(f"received:{response}")
        else:
            print("User rejected the file transfer request")

    @staticmethod
    def request_user_approval(sender_email, file_name, file_size):
        print(f"File transfer request from {sender_email}: {file_name} ({file_size} bytes)")

        # Prompt the user for approval
        response = input("Do you want to accept the file? (yes/no): ").lower()

        return response == 'yes'

    def handle_file_transfer_request(self, received_data):
        sender_email = received_data.get('sender_email', '')
        file_name = received_data.get('file_name', '')
        file_size = received_data.get('file_size', 0)

        # Notify the user about the incoming file and await their response
        user_response = self.request_user_approval(sender_email, file_name, file_size)

        status = 'approved' if user_response else 'rejected'

        if user_response:
            private_key_str, public_key_str, private_key, public_key = keyGen.generate_and_export_keypair()

            private_key_base64 = base64.b64encode(private_key_str).decode('utf-8')
            public_key_base64 = base64.b64encode(public_key_str).decode('utf-8')

            self.private_key: rsa.RSAPrivateKey = private_key
            response_data = {'status': status, 'key': public_key_base64}
            send_data(self.__socket, response_data)
            self.receive_file_transfer_requests()
        else:
            response_data = {'status': status}
            send_data(self.__socket, response_data)
        # Send the user's response back to the server

        # If approved, proceed with file transfer

    def handle_receive_chunk_request(self, received_data):
        sender_email = received_data.get('contact_email', '')
        file_name = received_data.get('file_name', '')
        encrypted_chunk = received_data.get('data', '')
        sequence_number = received_data.get('sequence', '')

        # Append chunk to file
        self.__file_being_sent.append(encrypted_chunk)

        sequence_number += 1

        # Send the user's response back to the server
        data = {'status': 'ok', 'sequence_number': sequence_number}
        print(f"Sending:{data}")
        self.__socket.sendall(json.dumps(data).encode())
        self.receive_file_transfer_requests()


    def receive_file_transfer_requests(self):
        # Check for incoming file transfer requests from the server
        data = receive_data(self.__socket)
        print(f"received in receive_file_transfer_requests{data}")
        if data and data.get('command') == 'file_transfer_request':
            self.handle_file_transfer_request(data)
        elif data and data.get('command') == 'receive_chunk':
            self.handle_receive_chunk_request(data)
        elif data and data.get('command') == 'reconstruct_file':
            self.handle_reconstruct_file_request(data)
        else:
            print("No file transfer requests at the moment.")

    def send_file_transfer_request(self, recipient_email, file_path):
        # Get file size for the request
        file_size = os.path.getsize(file_path)

        # Send file transfer request to the server
        data = {
            'command': 'request_file_transfer',
            'recipient_email': recipient_email,
            'file_name': os.path.basename(file_path),
            'file_size': file_size,
        }
        received_data = send_data(self.__socket, data)
        status = received_data.get('status', "")
        key = received_data.get('key', "")
        return status, key

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

    def handle_reconstruct_file_request(self, data):
        print("At reconstruct_file_request")
        file_name = data.get('file_name', '')
        sender_email = data.get('contact_email', '')

        # Make sure self.__file_being_sent is a list of strings
        if not self.__file_being_sent:
            print(f"No data for file {file_name} from {sender_email} to reconstruct.")
            return

        # # Filter chunks for the specified file and sender
        # file_chunks = [chunk for chunk in self.__file_being_sent if
        #                chunk['file_name'] == file_name and chunk['sender_email'] == sender_email]

        # Sort chunks by their sequence number

        # The final file path where the reconstructed file will be stored
        destination_path = os.path.join(os.getcwd(), f"{sender_email}_{file_name}")
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        print(self.__file_being_sent)
        # Write each chunk to the final file
        with open(destination_path, 'wb') as destination_file:
            for chunk in self.__file_being_sent:
                encrypted_data = chunk.encode('utf-8')
                # Decrypt the chunk here before writing to destination file
                self.private_key: rsa.RSAPrivateKey
                decrypted_chunk = self.private_key.decrypt(
                    encrypted_data,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    ))
                destination_file.write(decrypted_chunk)

        # Clean up the file entry in self.__file_being_sent
        self.__file_being_sent.clear()

        print(f"File {file_name} has been successfully reconstructed at {destination_path}.")


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
