
# ! do not have the serialization
import nanomsg

def start_client():
    # Create a REQ (request) socket
    client = nanomsg.Req()
    
    # Connect the socket to the server endpoint
    client.connect("tcp://127.0.0.1:5555")
    
    # Send a message to the server
    message = "Hello, server!"
    client.send(message.encode('utf-8'))
    
    # Receive a response from the server
    response = client.recv()
    print(f"Received from server: {response.decode('utf-8')}")
    
    client.close()

if __name__ == "__main__":
    start_client()
