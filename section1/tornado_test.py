import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!\n")

def make_app():
    routes = [
        (r"/", MainHandler)
    ]

    return tornado.web.Application(routes)


app = make_app()
app.listen(8888)
tornado.ioloop.IOLoop.current().start()