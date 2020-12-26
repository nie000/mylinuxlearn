from socketserver import TCPServer,StreamRequestHandler

ss_address = ("0.0.0.0",19534)

class MyTcpServer(StreamRequestHandler):

    def handle(self):

        self.wfile.write(b'get')


tcp_server = TCPServer(ss_address,MyTcpServer)

tcp_server.serve_forever()