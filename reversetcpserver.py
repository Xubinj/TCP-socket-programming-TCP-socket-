import socket
import select
import threading
import struct


def handle_client(client_socket, addr):
    """
    处理客户端连接，处理传入消息并发送相应的响应。
    """
    try:
        while True:
            # 读取头部（6字节）
            header = client_socket.recv(6)
            if len(header) < 6:
                break
            # 提取消息类型并相应处理
            msg_type, length = struct.unpack('!HI', header)
            if msg_type == 1:  # 初始化消息
                N = length  # N直接从length字段获取
                # 发送确认消息
                client_socket.sendall(struct.pack('!H', 2))
            elif msg_type == 3:  # 反转请求
                data = client_socket.recv(length)
                reversed_data = data[::-1]
                # 发送反转后的数据
                response = struct.pack('!HI', 4, len(reversed_data)) + reversed_data
                client_socket.sendall(response)
    finally:
        client_socket.close()


def start_server(server_ip, server_port):
    """
    启动服务器以监听传入的客户端连接。
    """
    # 创建并绑定UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f'Server listening on {server_ip}:{server_port}')

    while True:
        try:
            readable, _, _ = select.select([server], [], [], 0.1)
            for s in readable:
                client_socket, addr = s.accept()
                print(f'Connection established with {addr} ')
                client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
                client_handler.start()
        except KeyboardInterrupt:
            break
    server.close()


if __name__ == "__main__":
    # 配置服务器IP和端口
    start_server("0.0.0.0", 12333)
