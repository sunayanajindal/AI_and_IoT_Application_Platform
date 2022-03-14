import socket

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",1236))
with open("config.json",'w') as f:
    while 1:
        data = s.recv(1024).decode()
        if not data:
            break
        f.write(data)
s.close()
print("Config_file",'successfully downloaded.')