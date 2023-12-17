import socket
import json
from securedrop import SecureDrop
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


def send_data(client_socket, data):
    # Send data to the server
    client_socket.sendall(json.dumps(data).encode())

    # Receive the response from the server
    response_data = receive_data(client_socket)
    if response_data:
        print(f"Server response: {response_data}")
    return response_data


# Example usage
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(argv) >= 3:
    server_address = (argv[1], int(argv[2]))

    print(server_address)
else:
    server_address = ('localhost', 12345)
client_socket.connect(server_address)
user_id = "mark_schmidt@student.uml.edu"
mySecureDrop = SecureDrop(client_socket, user_id)
data = {'command': "add_connection_ids", 'data': user_id}
send_data(client_socket, data)
try:
    with open("contacts.json", 'r') as file:
        contact_json = json.load(file)
except FileNotFoundError or ValueError:
    contact_json = []
data = {'command': "record_contact.json", 'data': contact_json}
send_data(client_socket, data)
mySecureDrop.main_loop()
# Receive data from the server
# received_data = receive_data(client_socket)

# if received_data is not None:
#     # Extract encrypted text from the received data
#     encrypted_text = received_data.get("encrypted_text", "")
#
#     # Perform decryption on the client side
#     # decrypted_text = decrypt_text("key_file.key", encrypted_text)
#     # if decrypted_text is not None:
#     #     print("Decrypted Text:", decrypted_text)
#     # else:
#     #     print("Decryption failed.")
# else:
#     print("Error receiving or decoding data.")

# Close the connection
client_socket.close()