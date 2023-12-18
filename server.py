import json
import os
import socket
from cryptography.fernet import Fernet
import time
import socket
import threading
from sys import argv


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
        print(f"{data}")
        return None


def get_key_file_name(contact_email):
    # Construct the path to the contact's folder directly in the current working directory
    contact_folder = os.path.join(os.getcwd(), contact_email)

    # The key file is named 'name.bin' and is located inside the contact's folder
    key_file_name = os.path.join(contact_folder, "name.bin")

    return key_file_name


def handle_client(conn, addr, connections: list):
    print(f"New connection from {addr}")

    # Simulating server-initiated request by sending initial data to the client
    # initial_data = {"message": "Hello, client! This is a server-initiated message."}
    # conn.sendall(json.dumps(initial_data).encode())
    file_data = {}
    try:
        while True:
            # Receive the client's request
            received_data = receive_data(conn)

            if received_data is None:
                break

            command = received_data.get("command", "")

            if command == "list_contacts":
                # Get all contact.json of all people online
                # Simulating the list of online contacts
                data = received_data.get("data", "")
                client_contacts = []
                # contact_info = connections[-1]
                for single_connection_info in connections:
                    if single_connection_info["conn"] != conn:
                        for single_contact in single_connection_info["contacts"]:
                            print(f"Comparing {data} with {single_contact['UserID']}")
                            if data == single_contact['UserID']:
                                client_contacts.append(single_connection_info['userID'])
                response_data = {"contacts": client_contacts}
                conn.sendall(json.dumps(response_data).encode())

                # List to store contacts of the client

            elif command == "add_connection_ids":

                # Update the userID in connection_info
                data = received_data.get("data", "")

                for single_connection_info in connections:
                    if single_connection_info["conn"] == conn:
                        single_connection_info["userID"] = data

                response_data = {"response": "Connection id added successfully"}
                conn.sendall(json.dumps(response_data).encode())

            elif command == "record_contact.json":
                data = received_data.get("data", "")
                for single_connection_info in connections:
                    if single_connection_info["conn"] == conn:
                        single_connection_info["contacts"] = data
                response_data = {"response": "Contact json added successfully"}
                conn.sendall(json.dumps(response_data).encode())

            elif command == "send_chunk":
                # Process the incoming file chunk

                print(f"received:{received_data}")
                sequence_number = received_data.get('sequence', "")
                file_name = received_data.get('file_name', "")
                user_id = received_data.get('contact_email', "")  # This should be the sender's user ID
                encrypted_chunk = received_data.get('data', "").encode('utf-8')
                sequence_number += 1


                # Send the file to the recipient with a random seed for the sequence_number
                recipient_conn_info = next((info for info in connections if info["userID"] == user_id), None)
                if recipient_conn_info:
                    data = {
                        'command': 'receive_chunk',
                        'sequence': sequence_number,  # Random seed for the sequence_number
                        'data': encrypted_chunk.decode('utf-8'),  # JSON must be in text form
                        'file_name': file_name,
                        'contact_email': user_id
                    }
                    print(f"Sending:{data}")

                    # Send the chunk to the recipient
                    recipient_conn_info['conn'].sendall(json.dumps(data).encode())

                    # Wait for the recipient to acknowledge receipt
                    response = receive_data(recipient_conn_info['conn'])
                    print(f"response{response}")
                    if not response or response.get('status') != 'ok':
                        print("Failed to send chunk or recipient response was not okay.")
                        break
                    else:
                        print(f"Getting a response with sequence number {sequence_number}")
                # Decrypt the chunk
                # key_file_name = get_key_file_name(user_id)  # Implement this function
                # with open(key_file_name, "rb") as key_file:
                #     key = key_file.read()
                # cipher_suite = Fernet(key)
                # chunk = cipher_suite.decrypt(encrypted_chunk)

                # # Write the chunk to a temporary file
                # if (user_id, file_name) not in file_data:
                #     file_data[(user_id, file_name)] = open(f"{file_name}.part", 'wb')

                # # Append chunk to file
                # file_data[(user_id, file_name)].write(chunk)

                # Acknowledge the receipt of the chunk

                response_data = {'status': 'ok', 'sequence': sequence_number}
                conn.sendall(json.dumps(response_data).encode())

            elif command == "end_transfer":
                # Finalize file transfer
                print("end_transfer started")
                file_name = received_data.get('file_name')
                user_id = received_data.get('contact_email')  # This should be the sender's user ID
                sequence_number = received_data.get('sequence')

                # # Close the file
                # if (user_id, file_name) in file_data:
                #     file_data[(user_id, file_name)].close()
                #     del file_data[(user_id, file_name)]
                #
                # # Move the temporary file to its final destination
                # os.rename(f"{file_name}.part", f"received_{file_name}")

                # Acknowledge the completion of file transfer
                # Send the file to the recipient with a random seed for the sequence_number
                recipient_conn_info = next((info for info in connections if info["userID"] == user_id), None)
                if recipient_conn_info:

                        while True:

                            # Prepare the data to be sent
                            data = {
                                'command': 'reconstruct_file',
                                'sequence': sequence_number,  # Random seed for the sequence_
                                'file_name': file_name,
                                'contact_email': user_id
                            }

                            # # Send the chunk to the recipient
                            recipient_conn_info['conn'].sendall(json.dumps(data).encode())

                            # Wait for the recipient to acknowledge receipt
                            response = receive_data(recipient_conn_info['conn'])
                            if not response or response.get('status') != 'ok':
                                print("Failed to send chunk or recipient response was not okay.")
                                break
                            else:
                                print(f"Getting a response with sequence number {sequence_number}")

                            sequence_number += 1  # Increment the sequence number for each chunk

                else:
                    print(f"Recipient {user_id} is not online.")

                response_data = {'status': 'ok', 'message': 'File transfer complete.'}
                conn.sendall(json.dumps(response_data).encode())
            elif command == "request_file_transfer":
                recipient_email = received_data.get('recipient_email', '')
                file_name = received_data.get('file_name', '')
                file_size = received_data.get('file_size', 0)

                # Check if the recipient is online
                recipient_conn_info = next((info for info in connections if info["userID"] == recipient_email), None)

                if recipient_conn_info:
                    # Notify the recipient about the incoming file transfer
                    response_data = {
                        'command': 'file_transfer_request',
                        'sender_email': recipient_email,  # or use any sender identifier
                        'file_name': file_name,
                        'file_size': file_size,
                    }
                    recipient_conn_info['conn'].sendall(json.dumps(response_data).encode())
                    response = receive_data(recipient_conn_info['conn'])
                    if response and response['status'] == 'approved' or response['status'] == 'rejected':
                        conn.sendall(json.dumps(response).encode())
                else:
                    print(f"Recipient {recipient_email} is not online.")
            print(connections)

            time.sleep(5)  # Simulating some processing time

    except ConnectionResetError:
        print(f"Client {addr} disconnected abruptly.")

    finally:
        # Clean up resources associated with the client
        conn.close()
        print(f"Connection from {addr} closed.")
        # Remove the ID from user_contacts when the client disconnects
        user_id: str
        for conn_info in connections:
            if conn_info["conn"] == conn:
                connections.remove(conn_info)


def count_connections():
    while True:
        print(f"Number of connections: {len(connections)}")
        # Adjust the sleep time based on your requirements
        time.sleep(5)


# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(argv) >= 3:
    server_address = (argv[1], int(argv[2]))

    print(server_address)
else:
    server_address = ('localhost', 12345)
server_socket.bind(server_address)
server_socket.listen(5)

print("Server is waiting for connections...")

# List to keep track of connections
connections = []

# Thread to count the number of connections
count_thread = threading.Thread(target=count_connections)
count_thread.start()

while True:
    conn, addr = server_socket.accept()
    connection_info = {
        "conn": conn,
        "addr": addr,
        "userID": "Guest",
        "contacts": dict,
    }
    connections.append(connection_info)
    # Handle the client in a separate thread
    client_thread = threading.Thread(target=handle_client, args=(conn, addr, connections))
    client_thread.start()