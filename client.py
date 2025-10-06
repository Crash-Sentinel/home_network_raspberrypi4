def send_line(sock, text):
    sock.sendall((text + "\n").encode())

def recv_line(sock):
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()

def get_file(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        send_line(s, f"GET {filename}")
        response = recv_line(s)
        if response != "OK":
            print("Server error:", response)
            return
        size_line = recv_line(s)
        try:
            size = int(size_line)
        except ValueError:
            print("Invalid size line:", size_line)
            return
        received = 0
        with open(filename, "wb") as f:
            while received < size:
                data = s.recv(4096)
                if not data:
                    break
                f.write(data)
                received += len(data)
        print(f"Downloaded {filename} ({received} bytes)")
