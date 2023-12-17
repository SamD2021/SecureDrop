import os.path
import socket
import json
from securedrop import SecureDrop
from sys import argv
from userLogin import login, register


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


# Example usage
def main():
    userjson = os.path.join(os.getcwd(), 'users', "users.json")
    os.makedirs(os.path.join(os.getcwd(), 'users'),exist_ok=True)
    # Check if the path exists
    # Open file and check if any users registered

    try:
        with open(userjson, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        with open(userjson, "w") as file:
            file.write("[]")
            data = []
    # if file only has 2 charcters it is 'empty' just a placeholder
    if len(data) <= 0:
        print('No users are registered with this client.')
        s = input('Do you want to register a new user (y/n)?')

        # if do not want to register a user, quit
        if s == 'n':
            quit()
        # elif want to register a user, prompt the different info and take in user input
        elif s == 'y':
            register()
    else:
        user_id = login(data)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if len(argv) >= 3:
        server_address = (argv[1], int(argv[2]))

        print(server_address)
    else:
        server_address = ('localhost', 12345)
    client_socket.connect(server_address)
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
    client_socket.close()


main()
