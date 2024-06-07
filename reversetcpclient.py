import socket
import sys
import os
import random
import struct


def send_initialization(client_socket, N):
    """
    发送初始化消息给服务器。
    """
    message = struct.pack('!HI', 1, N)
    client_socket.sendall(message)
    response = client_socket.recv(2)
    if struct.unpack('!H', response)[0] == 2:
        print("连接建立成功")


def send_reverse_request(client_socket, block):
    """
    发送反转请求消息给服务器，并接收反转后的数据。
    """
    message = struct.pack('!HI', 3, len(block)) + block
    client_socket.sendall(message)
    header = client_socket.recv(6)
    msg_type, length = struct.unpack('!HI', header)
    if msg_type == 4:
        reversed_data = client_socket.recv(length)
        return reversed_data
    return None


def main(server_ip, server_port, file_path, Lmin, Lmax):
    """
    主函数，负责读取文件，分块发送数据并接收反转后的数据。
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    with open(file_path, 'rb') as file:
        data = file.read()

    # 生成各块的长度
    block_lengths = []
    total_length = len(data)
    while total_length > 0:
        if total_length < Lmin:
            block_length = total_length
        else:
            block_length = random.randint(Lmin, min(Lmax, total_length))
        block_lengths.append(block_length)
        total_length -= block_length

    N = len(block_lengths)
    send_initialization(client_socket, N)

    offset = 0
    all_reversed_data = []
    for i, length in enumerate(block_lengths):
        block = data[offset:offset + length]
        offset += length
        reversed_block = send_reverse_request(client_socket, block)
        all_reversed_data.append(reversed_block)
        print(f"第 {i + 1} 块：{reversed_block.decode('ascii')}")
    # 输出文本文件，该文件是原始文件的全部反转
    cnt = len(all_reversed_data)
    with open('reversed_' + os.path.basename(file_path), 'wb') as output_file:
        while cnt > 0:
            output_file.write(all_reversed_data[cnt - 1])
            cnt -= 1
    client_socket.close()


if __name__ == "__main__":
    # 命令行输入错误处理
    if len(sys.argv) != 6:
        print("用法: reversetcpclient.py <server_ip> <server_port> <file_path> <Lmin> <Lmax>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    file_path = sys.argv[3]
    Lmin = int(sys.argv[4])
    Lmax = int(sys.argv[5])

    main(server_ip, server_port, file_path, Lmin, Lmax)
