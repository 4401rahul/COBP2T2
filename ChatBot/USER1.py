# Here again we import required libraries
import threading
import socket

# Prompt the user to choose an alias for the chat
alias = input('Choose an alias >>> ')

# Create a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the chat server (server's IP and port)
client.connect(('127.0.0.1', 59000))

# Function to receive and process messages from the server
def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')  # Receive a message from the server
            if message == "alias?":
                client.send(alias.encode('utf-8'))  # Send the chosen alias to the server
            else:
                print(message)  # Print the received message to the client's console
        except:
            print('Error!')
            client.close()
            break

# Function to send messages to the server
def client_send():
    while True:
        message = f'{alias}: {input("")}'  # Compose a message including the user's alias
        client.send(message.encode('utf-8'))  # Send the message to the server

# Create a thread to run the client_receive function
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

# Create a thread to run the client_send function
send_thread = threading.Thread(target=client_send)
send_thread.start()
