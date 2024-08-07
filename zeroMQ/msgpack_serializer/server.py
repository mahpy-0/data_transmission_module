
# ? in this one the image deserialize and save's 
import zmq
import msgpack

def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")
    
    print("Server is running and waiting for requests...")
    
    while True:
        try:
            # Receive the serialized image data
            data = socket.recv()
            
            # Deserialize the received data
            unpacked_data = msgpack.unpackb(data, raw=False)
            image_data = unpacked_data['image']

            # Save the image
            with open('received_image.jpg', 'wb') as f:
                f.write(image_data)

            print("Image received and saved.")

            # Send a response
            response = "Image received"
            socket.send_string(response)
        except KeyboardInterrupt:
            print("Server interrupted by user.")
            break

    socket.close()
    context.term()
    print("Server closed.")

if __name__ == "__main__":
    start_server()
