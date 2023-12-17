import json
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
        return None


def handle_client(conn, addr, connections: list):
    print(f"New connection from {addr}")

    # Simulating server-initiated request by sending initial data to the client
    #initial_data = {"message": "Hello, client! This is a server-initiated message."}
    #conn.sendall(json.dumps(initial_data).encode())

    try:
        while True:
            # Receive the client's request
            received_data = receive_data(conn)

            if received_data is None:
                break

            command = received_data.get("command", "")
            data = received_data.get("data", "")

            if command == "list_contacts":
                # Get all contact.json of all people online
                # Simulating the list of online contacts
                client_contacts = []
                #contact_info = connections[-1]
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

                for single_connection_info in connections:
                    if single_connection_info["conn"] == conn:
                        single_connection_info["userID"] = data

                response_data = {"response": "Connection id added successfully"}
                conn.sendall(json.dumps(response_data).encode())

            elif command == "record_contact.json":
                for single_connection_info in connections:
                    if single_connection_info["conn"] == conn:
                        single_connection_info["contacts"] = data
                response_data = {"response": "Contact json added successfully"}
                conn.sendall(json.dumps(response_data).encode())

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