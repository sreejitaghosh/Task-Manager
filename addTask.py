import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from taskdata import taskdata
from taskBoarddata import taskBoarddata

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class addTask(webapp2.RequestHandler):
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
            self.redirect('/')

        TaskBoardName = self.request.get('taskBoarddata')
        OwnerName = self.request.get('email')
        data = ndb.Key('taskBoarddata', TaskBoardName+""+OwnerName).get()

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'data' : data
        }

        template = JINJA_ENVIRONMENT.get_template('addTask.html')
        self.response.write(template.render(template_values))

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

        TaskBoardName = self.request.get('taskBoarddata')
        OwnerName = self.request.get('email')
        TaskNameFromUser = self.request.get('TaskName')
        Due_Date = self.request.get('Due_Date')
        Unique = TaskBoardName+""+OwnerName # task key
        self.response.write(Unique)
        element = []
        in_List = False

        data = ndb.Key('taskBoarddata',Unique).get()
        TaskData = ndb.Key('taskdata',Unique).get()
        if TaskData != None:
            element = TaskData.Title

            i = 0
            while i < len(element):
                if element[i] == TaskNameFromUser:
                    in_List = True
                    break
                else:
                    in_List = False
                    i = i + 1

        if in_List == True:
            self.redirect('/')
        else:
            if len(element) == 0:
                add_data = taskdata(id=Unique)
                add_data.Title.append(TaskNameFromUser)
                add_data.Due_Date.append(Due_Date)
                add_data.Task_Completion.append("Not Complete")
                add_data.Task_assigned.append("Not Assigned")
                add_data.Date.append("Not Complete")
                add_data.Time.append("Not Complete")
                add_data.put()
                self.redirect('/invite?taskBoarddata='+TaskBoardName+'&email='+OwnerName)
            else:
                add_data = ndb.Key('taskdata',Unique).get()
                add_data.Title.append(TaskNameFromUser)
                add_data.Due_Date.append(Due_Date)
                add_data.Task_Completion.append("Not Complete")
                add_data.Task_assigned.append("Not Assigned")
                add_data.Date.append("Not Complete")
                add_data.Time.append("Not Complete")
                add_data.put()
                self.redirect('/invite?taskBoarddata='+TaskBoardName+'&email='+OwnerName)

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'data' : data
            }

        template = JINJA_ENVIRONMENT.get_template('addTask.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/addTask', addTask)
], debug=True)
