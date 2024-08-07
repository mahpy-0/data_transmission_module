
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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 9999))

try:
    # simple_data = {
    #     "key1": "data1",
    #     "key2": "data2",
    #     "key3": "data3",
    # }
    # serialized_simple_data = pickle.dumps(simple_data)

    test_1 = Test("mamad")
    serialized_simple_data = pickle.dumps(test_1)
    print(serialized_simple_data)

    client.sendall(serialized_simple_data)
    print("sent!!!")
finally:
    client.close()
