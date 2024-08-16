
# ! do nat have serialization
import zmq

def start_server():
    # Create a ZeroMQ context
    context = zmq.Context()
    
    # Create a REP (reply) socket
    socket = context.socket(zmq.REP)
    
    # Bind the socket to an endpoint
    socket.bind("tcp://127.0.0.1:5555")
    
    print("Server is running and waiting for requests...")
    
    while True:
        try:
            # Receive a message from the client
            message = socket.recv_string()
            print(f"Received: {message}")
            
            # Send a response back to the client
            response = "Hello World"
            socket.send_string(response)
            
        except KeyboardInterrupt:
            print("Server interrupted by user.")
            break

    # Close the socket and terminate the context
    socket.close()
    context.term()
    print("Server closed.")

if __name__ == "__main__":
    start_server()
