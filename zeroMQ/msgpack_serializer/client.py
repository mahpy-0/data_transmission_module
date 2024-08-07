
# ? in this one the image deserialize and save's  
import zmq
import msgpack

def start_client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")

    # Load the image
    with open('example_image.jpg', 'rb') as f:
        image_data = f.read()

    # Serialize the image data
    packed_data = msgpack.packb({'image': image_data}, use_bin_type=True)

    # Send the serialized image data
    socket.send(packed_data)

    # Receive a response
    response = socket.recv_string()
    print(f"Received from server: {response}")

    socket.close()
    context.term()

if __name__ == "__main__":
    start_client()
