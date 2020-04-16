import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from taskBoarddata import taskBoarddata
from addTaskBoard import addTaskBoard
from taskBoard import taskBoard


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class invite(webapp2.RequestHandler):
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
        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'available_email_id' : available_email_id,
             'taskboard_data' : taskboard_data
        }

        template = JINJA_ENVIRONMENT.get_template('invite.html')
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

        call_tb = self.request.get('taskBoarddata')
        call_user = self.request.get('email')
        all_call = call_tb+""+call_user
        user_select_email = self.request.get('select_email_id')
        taskBoard_a = ndb.Key('taskBoarddata',all_call).get()
        if taskBoard_a.owner == user.email():
            section = False
            new_myuser = ndb.Key('MyUser',user_select_email).get()

            if new_myuser != None:
                call = new_myuser.taskboard
                i = 0
                while i < len(call):
                    if call[i] == all_call:
                        section = True
                        break
                    else:
                        section = False
                        i = i + 1

            if section == True:
                self.redirect('/')
            else:
                if all_call != None:
                    new_myuser.taskboard.append(all_call)
                    new_myuser.put()
                    taskBoard_a.email_address.append(user_select_email)
                    taskBoard_a.put()
                    self.redirect('/taskBoard')
                else:
                    self.redirect('/')
        else:
            self.redirect('/')

        available_email_id = MyUser.query().fetch()
        taskboard_data = ndb.Key('taskBoarddata',all_call).get()

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
    ('/invite', invite)
], debug=True)
