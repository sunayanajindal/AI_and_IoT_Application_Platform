import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1",1236))
s.listen(100)

c, addr = s.accept()
print(c)

file = open("sample_config.json",'rb')
data = file.read(1024)
while data:
    c.send(data)
    data = file.read(1024)