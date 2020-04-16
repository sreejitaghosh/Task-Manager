import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from taskBoarddata import taskBoarddata

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class addTaskBoard(webapp2.RequestHandler):
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
            self.redirect('/')

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user
        }

        template = JINJA_ENVIRONMENT.get_template('addTaskBoard.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
        user = users.get_current_user()

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
            self.redirect('/')

        TaskBoardNameFromUser = self.request.get('TaskBoardName')
        Unique = TaskBoardNameFromUser+""+user.email()
        data = ndb.Key('MyUser', user.user_id()).get()

        element = data.taskboard
        in_List = False
        i = 0
        while i < len(element):
            if element[i] == Unique:
                in_List = True
                break
            else:
                in_List = False
                i = i + 1

        if in_List == True:
            self.redirect('/')
        else:
            add_data = taskBoarddata(id=Unique)
            add_data.owner = user.email()
            add_data.taskBoarddata = TaskBoardNameFromUser
            add_data.put()
            data.taskboard.append(Unique)
            data.put()
            self.redirect('/')

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'Value_data' : data
            }

        template = JINJA_ENVIRONMENT.get_template('addTaskBoard.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/addTaskBoard', addTaskBoard)
], debug=True)
