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

class editTask(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
        taskBoard = self.request.get('taskBoarddata')
        email = self.request.get('email')
        taskBoard_key = taskBoard+""+email
        user = users.get_current_user()
        available_email_id = []

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
            self.redirect('/')

        available_email_id = MyUser.query().fetch()
        taskboard_data = ndb.Key('taskBoarddata',taskBoard_key).get()

        task_data = ndb.Key('taskdata',taskBoard_key).get()
        if task_data != None:
            length_task_data = len(task_data.Title)

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'available_email_id' : available_email_id,
             'taskboard_data' : taskboard_data,
             'task_data' : task_data
        }

        template = JINJA_ENVIRONMENT.get_template('editTask.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
        taskBoard = ''
        add = ''
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
            self.redirect('/')

        tb = self.request.get('taskBoarddata')
        owner = self.request.get('email')
        unique = tb+""+owner
        select_task_owner = self.request.get('select_task_owner')
        taskTitleName = self.request.get('taskTitleName')
        ButtonOption = self.request.get('Button')
        available_email_id = MyUser.query().fetch()
        taskboard_data = ndb.Key('taskBoarddata',unique).get()

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'available_email_id' : available_email_id,
            'taskboard_data' : taskboard_data
        }

        template = JINJA_ENVIRONMENT.get_template('invite.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/editTask',editTask),
], debug=True)
