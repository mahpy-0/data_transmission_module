
# ? in this one the image deserialize and save's 
import nanomsg
import msgpack

def start_server():
    server = nanomsg.Rep()
    server.bind("tcp://127.0.0.1:5555")
    print("Server is running and waiting for requests...")

    while True:
        try:
            # Receive the message
            data = server.recv()
            
            # Deserialize the received data
            unpacked_data = msgpack.unpackb(data, raw=False)
            image_data = unpacked_data['image']

            # Save the image
            with open('received_image.jpg', 'wb') as f:
                f.write(image_data)

            print("Image received and saved.")

            # Send a response
            response = "Image received"
            server.send(response.encode('utf-8'))
        except KeyboardInterrupt:
            print("Server interrupted by user.")
            break

    server.close()
    print("Server closed.")

if __name__ == "__main__":
    start_server()
