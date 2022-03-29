from socket import *
serverPort = 6500
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.setblocking(500)
serverSocket.listen()
print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    ip = addr[0]
    port = addr[1]
    phone_list = {}
    a_file = open("list.txt")
    for line in a_file:
        key, value = line.split(",")
        phone_list[key] = int(value)
    a_file.close()
    req = connectionSocket.recv(1024).decode()
    print(req)
    myReq = req[4:req.find(" ", 4) + 1]
    if myReq == '/' or 'index.html' in myReq or 'main.html' in myReq:
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send(b"Content-Type: text/html\r\n")
        html = open("main.html", "rb")
        css = open("main.css", "rb")
        connectionSocket.sendfile(html)
        connectionSocket.sendfile(css)
        html.close()
        css.close()
        connectionSocket.send("\r\n".encode())
    elif 'error.html' in myReq:
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send(b"Content-Type: text/html\r\n")
        connectionSocket.send("\r\n".encode())
        connectionSocket.sendfile(open("error.html", "rb"))
        connectionSocket.sendfile(open("error.css", "rb"))
    elif 'image.jpg' in myReq:
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send(b"Content-Type: image/jpeg\r\n")
        connectionSocket.send("\r\n".encode())
        connectionSocket.sendfile(open("image.jpg", "rb"))
    elif 'logo.png' in myReq:
        connectionSocket.send(f"HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send(f"Content-Type: image/png\r\n".encode())
        img = open("logo.png", "rb")
        r = img.read()
        img.close()
        connectionSocket.send(f"\r\n".encode())
        connectionSocket.send(r)

    elif 'error.png' in myReq:
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send(b"Content-Type: image/png\r\n")
        connectionSocket.send("\r\n".encode())
        connectionSocket.sendfile(open("error.png", "rb"))
    elif 'SortByPrice' in myReq:
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/plain\r\n".encode())
        sorted_list = sorted(phone_list.items(), key=lambda x: x[1])
        with open("sorted.txt", "w") as f:
            for key in sorted_list:
                f.write(f"{key}\n")
        file = open("sorted.txt", "r")
        content = file.read()
        file.close()
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(content.encode())
    elif 'SortByName' in myReq:
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/plain\r\n".encode())
        sorted_list2 = sorted(phone_list.items())
        with open("sorted2.txt", "w") as f:
            for key in sorted_list2:
                f.write(f"{key}\n")
        file = open("sorted2.txt", "r")
        content2 = file.read()
        file.close()
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(content2.encode())
    elif 'html' in myReq:
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send(b"Content-Type: text/html\r\n")
        html = open("main.html", "rb")
        r = html.read()
        html.close()
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(r)

    elif 'css' in myReq:
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send(f"Content-Type: text/css\r\n".encode())
        css = open("main.html", "rb")
        r = css.read()
        css.close()
        connectionSocket.send(f"\r\n".encode())
        connectionSocket.send(r)

    else:
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n")
        connectionSocket.send(b"Content-Type: text/html\r\n")
        connectionSocket.send((open("error.html", "r").read() + "<footer> IP: "
                               + gethostbyname(gethostname())
                               + "PORT:" + str(port)
                               + "</footer>"
                               + open("error.css", "r").read()).encode())
        connectionSocket.send("\r\n".encode())

    connectionSocket.close()
