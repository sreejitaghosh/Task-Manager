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
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
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
        taskTitle = self.request.get('EditButton')
        taskboard_data = ndb.Key('taskBoarddata',unique).get()
        task_data = ndb.Key('taskdata',unique).get()
        taskdata = []

        for i in range(0,len(task_data.Title)):
            if task_data.Title[i] == taskTitle:
                taskdata.append(task_data.Title[i])
                taskdata.append(task_data.Due_Date[i])
        editButtonValue = self.request.get('submit')

        if editButtonValue == 'Edit':
            TaskOldName = self.request.get('TaskOldName')
            TaskNewName = self.request.get('TaskNewName')
            TaskNewDue_Date = self.request.get('TaskNewDue_Date')
            for i in range(0,len(task_data.Title)):
                if task_data.Title[i] == TaskOldName:
                    task_data.Title[i] = TaskNewName
                    task_data.Due_Date[i] = TaskNewDue_Date
                    task_data.put()
                    self.redirect('/invite?taskBoarddata='+tb+'&email='+owner)

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'taskboard_data' : taskboard_data,
            'taskdata' : taskdata
        }

        template = JINJA_ENVIRONMENT.get_template('editTask.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/editTask',editTask),
], debug=True)
