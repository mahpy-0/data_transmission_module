
# ? in this one the image deserialize and save's 
import socket
import msgpack

def start_client():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the server's address and port
    server_address = ('127.0.0.1', 5555)
    client_socket.connect(server_address)
    
    try:
        # Load the image
        with open('example_image.jpg', 'rb') as f:
            image_data = f.read()
        
        # Serialize the image data
        packed_data = msgpack.packb({'image': image_data}, use_bin_type=True)
        
        # Send the serialized image data
        client_socket.sendall(packed_data)
        
        # Receive a response from the server
        response = client_socket.recv(1024)
        print(f"Received from server: {response.decode('utf-8')}")
    
    finally:
        # Clean up the connection
        client_socket.close()

if __name__ == "__main__":
    start_client()
