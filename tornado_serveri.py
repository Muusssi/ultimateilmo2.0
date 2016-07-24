import tornado.ioloop
import tornado.web
import tornado.httpserver
import os
import database as db
import sys

from psycopg2 import IntegrityError

APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
STATIC_DIRECTORY = os.path.abspath(os.path.join(APP_DIRECTORY, 'static'))
TEMPLATES_DIRECTORY = os.path.abspath(os.path.join(APP_DIRECTORY, 'templates'))



class Application(tornado.web.Application):
    def __init__(self, database):
        handlers = [
                (r"/", MainPageHandler),
                (r"/answer/([0-9]+)", AnswerHandler),
                (r"/new_player", NewPlayerHandler),
            ]

        settings = dict(
                template_path=TEMPLATES_DIRECTORY,
                static_path=STATIC_DIRECTORY,
                debug=True,
            )

        self.database = database
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.database


class MainPageHandler(BaseHandler):
    def get(self):
        self.render("ilmo.html",
                players=self.db.people(),
                answers=self.db.answers(),
            )

class AnswerHandler(BaseHandler):
    def get(self, person_id):
        self.render("answer.html",
                player=self.db.person(person_id),
                answer=self.db.answer(person_id),
            )

    def post(self, person_id):
        self.db.register_answer(
                self.get_argument('person_id'),
                self.get_argument('notes'),
                self.get_arguments('time'),
            )
        self.redirect("/")

class NewPlayerHandler(BaseHandler):
    def get(self):
        self.render("new_player.html",
                name='',
                error='',
            )

    def post(self):
        name = self.get_argument('name')
        if name:
            try:
                self.db.register_player(name)
                self.redirect("/")
            except IntegrityError:
                self.render("new_player.html",
                name=name,
                error='Nimi varattu',
            )
        else:
            self.render("new_player.html",
                name=name,
                error='Nimi puuttuu',
            )





if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print "error: missing password"
        exit(0)

    httpserver = tornado.httpserver.HTTPServer(Application(db.Database(sys.argv[1])))
    httpserver.listen(8080)
    tornado.ioloop.IOLoop.current().start()

