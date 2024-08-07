
# ? in this one the image deserialize and save's 
import nanomsg
import msgpack

def start_client():
    client = nanomsg.Req()
    client.connect("tcp://127.0.0.1:5555")

    # Load the image
    with open('example_image.jpg', 'rb') as f:
        image_data = f.read()

    # Serialize the image data
    packed_data = msgpack.packb({'image': image_data}, use_bin_type=True)

    # Send the serialized image data
    client.send(packed_data)

    # Receive a response
    response = client.recv()
    print(f"Received from server: {response.decode('utf-8')}")

    client.close()

if __name__ == "__main__":
    start_client()
