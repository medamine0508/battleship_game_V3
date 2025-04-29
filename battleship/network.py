import socket
import pickle

class NetworkManager:
    def __init__(self, is_server=False, host='localhost', port=5555):
        self.is_server = is_server
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        
    def start_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Server started on {self.host}:{self.port}")
        self.connection, addr = self.socket.accept()
        print(f"Connected to {addr}")

    def connect_to_server(self):
        print(f"Connecting to {self.host}:{self.port}...")
        self.socket.connect((self.host, self.port))
        print("Connected successfully!")
        self.connection = self.socket

    def send(self, data):
        try:
            serialized = pickle.dumps(data)
            self.connection.sendall(serialized)
        except (socket.error, pickle.PickleError) as e:
            print(f"Network error: {e}")
            return False
        return True

    def receive(self):
        try:
            data = self.connection.recv(4096)
            if not data:
                return None
            return pickle.loads(data)
        except (socket.error, pickle.PickleError) as e:
            print(f"Network error: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
        self.socket.close()