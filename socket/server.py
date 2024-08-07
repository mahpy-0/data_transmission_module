
# ! do not have the msgpack serialization
import socket
import pickle

class Test:
    """
    test class for sending objects over network testing
    """
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return self.name

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 9999))

server.listen(1)

while True:
    print("waiting for connection...")
    client, addr = server.accept()

    try:
        print("connected")

        data = b""
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            data += chunk

        print(f"Reeceived: {data}")

        deserialized_data = pickle.loads(data)
        print(f"Reeceived: {deserialized_data}")
    finally:
        client.close()
