
# ? in this one the image deserialize and save's 
import socket
import msgpack

def start_server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address and port
    server_address = ('127.0.0.1', 5555)
    server_socket.bind(server_address)
    
    # Listen for incoming connections
    server_socket.listen(1)
    print("Server is running and waiting for connections...")
    
    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()
        
        try:
            # Receive the data from the client
            data = b''
            while True:
                chunk = connection.recv(4096)
                if not chunk:
                    break
                data += chunk
            
            # Deserialize the received data
            unpacked_data = msgpack.unpackb(data, raw=False)
            image_data = unpacked_data['image']
            
            # Save the image
            with open('received_image.jpg', 'wb') as f:
                f.write(image_data)
            
            print("Image received and saved.")
            
            # Send a response to the client
            response = "Image received"
            connection.sendall(response.encode('utf-8'))
        
        finally:
            # Clean up the connection
            connection.close()

if __name__ == "__main__":
    start_server()
