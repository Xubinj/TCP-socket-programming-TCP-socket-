# TCP Socket Programming
## 文件列表
- reversetcpserver.py：服务器端代码
- reversetcpclient.py：客户端代码
- readme.txt：运行说明文档

## 运行环境
- Python 3.x
- 支持socket库和threading库

## 配置选项
- 客户端启动命令行格式：
python3 reversetcpclient.py <server_ip> <server_port> <file_path> <Lmin> <Lmax>
例如：
python3 reversetcpclient.py 192.168.1.100 12345 testfile.txt 10 100

- 服务器启动命令行格式：
python3 reversetcpserver.py

## 运行步骤
- 在服务器端运行 reversetcpserver.py，启动服务器。
- 在客户端运行 reversetcpclient.py，指定服务器 IP 地址和端口，ASCII 文件路径，最小块大小 Lmin，最大块大小 Lmax。
- 客户端会发送 Initialization 报文请求服务器连接，接收 agreement 报文确认连接建立。
- 客户端会随机分块发送 reverseRequest 报文，服务器处理后返回 reverseAnswer 报文。
- 客户端收到反转后的数据块并显示在终端，同时生成反转后的完整文件。

## 功能说明
- 服务器和客户端通过TCP连接进行通信。
- 客户端读取指定文件并随机分块发送给服务器。
- 服务器对接收到的每个块进行反转，并返回给客户端。
- 客户端在接收到反转后的数据后，打印每个块的内容。
