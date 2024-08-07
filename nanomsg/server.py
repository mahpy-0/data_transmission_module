
# ! do not have the serialization
import nanomsg
import time

def start_server():
    # Create a REP (reply) socket
    server = nanomsg.Rep()
    
    # Bind the socket to an endpoint
    server.bind("tcp://127.0.0.1:5555")
    
    print("Server is running and waiting for requests...")
    
    while True:
        try:
            # Receive a message from the client
            message = server.recv()
            print(f"Received: {message.decode('utf-8')}")
            
            # Send a response back to the client
            response = "Message received"
            server.send(response.encode('utf-8'))
            
        except KeyboardInterrupt:
            print("Server interrupted by user.")
            break

    server.close()
    print("Server closed.")

if __name__ == "__main__":
    start_server()
