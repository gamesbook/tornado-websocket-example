from tornado import websocket, web, ioloop
import json

cl = []
clients = []

def send_to_all_clients(msg):
    for client in clients:
        client.write_message(message)

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        send_to_all_clients("new client")
        clients.append(self)
        if self not in cl:
            cl.append(self)

    def on_message(self, message):
        for client in clients:
            client.write_message(message)

    def on_close(self):
        clients.remove(self)
        send_to_all_clients("removing client")
        if self in cl:
            cl.remove(self)

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
