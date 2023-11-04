# Here we Build a simple chat application that allows multiple users to communicate in real-time using python.

#By Rahul Joshi

# First we import required libraries
import threading
import socket

# Now we define the server's host and port
host = '127.0.0.1'  # Server's IP address (in this case, localhost)
port = 59000  # Port to listen for client connections

# Now we create a socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server.bind((host, port))

# To Start listening for incoming connections
server.listen()

# Now we Initialize lists to store connected clients and their aliases
clients = []
aliases = []

# Function to broadcast a message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle each connected client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)  # Receive a message from the client
            broadcast(message)  # Broadcast the message to all clients
        except:
            # If an error occurs (e.g., the client disconnects), remove the client and their alias
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

# Main function to accept and manage client connections
def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()  # Accept a new client connection
        print(f'Connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))  # Request the client to provide an alias
        alias = client.recv(1024)  # Receive the client's chosen alias
        aliases.append(alias)  # Store the alias
        clients.append(client)  # Store the client
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('You are now connected!'.encode('utf-8'))
        # Start a new thread to handle this client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Entry point of the script
if __name__ == "__main__":
    receive()  # Start the server and begin accepting client connections
