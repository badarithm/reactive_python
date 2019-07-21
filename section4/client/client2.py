from asyncio
from random import choice

from rx import Observable
from rx.subjects import Subject
from rx.concurrency import IOLoopScheduler

from tornado.ioloop import IOLoop
from tornado.websocket import websocket_connect

class Client:
    def __init__(self, host = 'localhost', port = 8888):
        self.url = 'ws://{}/{}/exchange'.format(host, port)
        self.conn = None
        self.opened = Subject()
        self.messages = Subject()

    def write_message(self, message):
        self.conn.w

    def connect(self):
        def on_message_callback(message):
            self.messages.on_next(message)

        def on_connect(connection):
            self.conn = connection
            self.opened.on_next(connection)
            self.opened.on_completed()
            self.opened.dispose()

        future = websocket_connect(self.url, on_message_callback=on_message_callback)
        Observable.from_future(future).subscribe(on_connect)

if '__main__' == __name__:
    scheduler = IOLoopScheduler(IOLoop.current())
    def make_say_hello(client, i):
        def say_hello():
            client.write_message('Hello World, {}!'.format(i))

        def schedule_say_hello(conn):
            Observable.interval(choice([300, 500, 1000, 2000, 3000]), scheduler=scheduler).subscribe(lambda _: say_hello())
        return schedule_say_hello

    for i in range(10):
        client = Client()
        client.messages.subscribe(lambda message: print(message))
        client.opened.subscribe(lambda conn: print('Connection opened to server'))
        client.opened.subscribe(make_say_hello(client, i))
        client.connect()
    IOLoop.current().start()