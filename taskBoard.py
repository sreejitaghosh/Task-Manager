import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from taskBoarddata import taskBoarddata
from addTaskBoard import addTaskBoard


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class taskBoard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
        taskBoard = ''
        add = ''
        user = users.get_current_user()
        data = []

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            myuser_details = ndb.Key('MyUser', user.user_id())
            myuser = myuser_details.get()
            if myuser == None:
                myuser = MyUser(id=user.user_id())
                myuser.email_address = user.email()
                welcome = 'Welcome to the application'
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        all_values = myuser.taskboard
        i = 0
        while i < len(all_values):
            taskboard_NameValue = ndb.Key('taskBoarddata', all_values[i]).get()
            data.append(taskboard_NameValue)
            i = i + 1

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'Value_data' : data
        }

        template = JINJA_ENVIRONMENT.get_template('taskBoard.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/taskBoard', taskBoard)
], debug=True)
