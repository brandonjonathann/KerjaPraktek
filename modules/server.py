import socket

# Initialize the current IP Address of the machine.
HOST = socket.gethostbyname(socket.gethostname())

MIN_PORT = 0
MAX_PORT = 65565

# Timeout for port check in seconds.
PORT_CHECK_TIMEOUT = 1

def find_open_port():
    """
    Function to find an open port in the range [MIN_PORT, MAX_PORT].

    Returns the first open port found, or None if no open port is found.
    """

    # Loop through a range of ports to find an open port.
    for port in range(MIN_PORT, MAX_PORT):
        try:

            # Create a socket as a client for checking.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

                # Limit the time to check a port.
                client.settimeout(PORT_CHECK_TIMEOUT)

                # Bind and connect the client to the port being checked.
                client.bind((HOST, port))
                client.connect((HOST, port))

                # If the connection succeeds, close the 
                # client and return the open port.
                return port
        
        except:

            # If a port is not open, continue to the next port.
            pass
    
    # Return None if no open port is found.
    return None
    
def receive_data(client: socket, file_name: str):
    with open(file_name, "wb") as file:
        file_in_bytes = b""

        while True:
            data_chunk = client.recv(1024)
            if file_in_bytes[-5:] == b"<END>":
                break
            else:
                file_in_bytes += data_chunk

        file.write(file_in_bytes[:-5])
            

def start_server(port: int, new_files: list):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, port))
    server.listen()
    print(f'Server is listening.')

    importing = True

    while importing:
        client, address = server.accept()
        print(f'Server accepted a client.')
        file_name = client.recv(1024).decode()
        print(file_name)

        if file_name == 'process ender':
            print(f'Import process is terminated, closing server.')
            importing = False

        else:
            receive_data(client, file_name)
            client.close()
            new_files.append(file_name)

    server.close()

def end_server(port: int):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, port))

    client.send("process ender".encode())
