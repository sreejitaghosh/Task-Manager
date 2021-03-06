import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from taskdata import taskdata
from taskBoarddata import taskBoarddata
from taskBoard import taskBoard
from addTask import addTask
from addTaskBoard import addTaskBoard
from invite import invite
from AssignValue import AssignValue
from Complete import Complete
from Incomplete import Incomplete
from editTask import editTask
from DeleteTask import DeleteTask

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
        taskBoard = ''
        addTask = ''
        addTaskBoard = ''

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            myuser_details = ndb.Key('MyUser', user.email())
            myuser = myuser_details.get()
            if myuser == None:
                myuser = MyUser(id=user.email())
                myuser.email_address = user.email()
                welcome = 'Welcome to the application'
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user
        }

        template = JINJA_ENVIRONMENT.get_template('login-logout.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/taskBoard',taskBoard),
    ('/addTask',addTask),
    ('/addTaskBoard',addTaskBoard),
    ('/invite',invite),
    ('/AssignValue',AssignValue),
    ('/Complete',Complete),
    ('/Incomplete',Incomplete),
    ('/editTask',editTask),
    ('/deleteTask',DeleteTask)
], debug=True)
