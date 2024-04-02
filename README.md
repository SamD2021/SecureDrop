
# SecureDrop

SecureDrop is a secure messaging and file transfer system designed to provide confidentiality, integrity, and authenticity of data exchanged between clients. It ensures that sensitive information remains protected during transmission over the network.

## Features

- **User Authentication**: SecureDrop requires users to authenticate themselves before accessing the system, ensuring that only authorized users can send and receive messages and files.
- **End-to-End Encryption**: All communications between clients and the server are encrypted to prevent eavesdropping and tampering by unauthorized parties.
- **Password Salting**: SecureDrop uses password salting to enhance the security of user passwords stored in the system, making them resistant to brute-force attacks.
- **File Transfer**: SecureDrop supports secure file transfer between clients, allowing users to share files with each other while ensuring confidentiality and integrity.
- **Multi-Platform Compatibility**: SecureDrop is implemented in Python, making it compatible with various operating systems such as Windows, Linux, and macOS.

## Installation

1. Clone the SecureDrop repository to your local machine:

   ```
   git clone https://github.com/your-username/securedrop.git
   ```

2. Navigate to the project directory:

   ```
   cd securedrop
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

### Server

1. Start the SecureDrop server by running `server.py`:

   ```
   python server.py
   ```

2. The server will start listening for incoming connections from clients.

### Client

1. Run `client.py` to start the SecureDrop client:

   ```
   python client.py
   ```

2. Follow the prompts to log in or register a new user.

3. Once logged in you can transfer files, and interact with other users securely.

## Contributors

- SamD2021 (@SamD2021)
- MarkSchmidt (@markschmidt-ship-it)
- PaigeMarie

