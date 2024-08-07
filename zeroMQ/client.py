
# ! do nat have serialization
import zmq

def start_client():
    # Create a ZeroMQ context
    context = zmq.Context()
    
    # Create a REQ (request) socket
    socket = context.socket(zmq.REQ)
    
    # Connect the socket to the server endpoint
    socket.connect("tcp://127.0.0.1:5555")
    
    # Send a message to the server
    message = "Hello, server!"
    socket.send_string(message)
    
    # Receive a response from the server
    response = socket.recv_string()
    print(f"Received from server: {response}")

    # Close the socket and terminate the context
    socket.close()
    context.term()

if __name__ == "__main__":
    start_client()
