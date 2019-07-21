from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from rx.concurrency import IOLoopScheduler
from rx import Observable
from rx.subjects import Subject

class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, Stock Exchange\n")

class ExchangeHandler(WebSocketHandler):
    def open(self):
        Server.messages.on_next(['opened', self.request])

    def on_message(self, message):
        Server.messages.on_next(['message', message])

    def on_close(self) -> None:
        Server.messages.on_next(['closed', self.request])


class Server:
    instance = None

    class __Server:
        def __init__(self):
            scheduler = IOLoopScheduler(IOLoop.current())
            self.messages = Subject()
            only_messages = self.messages.filter(lambda message: message[0] == 'message')\
                .map(lambda message : message[1])\
                .publish()

            only_messages.subscribe(lambda message: print(message))
            only_messages.connect()

            self.__app = Application([
                (r'/exchange', ExchangeHandler),
                (r'/', MainHandler),
            ])

        def start(self):
            self.__app.listen(8888)

    def __init__(self, *args, **kwargs):
        if None is Server.instance:
            Server.instance = Server.__Server()

    def __getattr__(self, item):
        return getattr(self.instance, item)

if '__main__' == __name__:
    Server().messages.subscribe(lambda message: print('Received {}'.format(message)))
    Server().messages.filter(lambda message: message[0] == 'open').subscribe(lambda message: print('Connection is open {}'.format(message)))
    Server().start() # because getattr is used to access properties from  __Server class
    IOLoop.current().start()