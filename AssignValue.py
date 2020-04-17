import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class AssignValue(webapp2.RequestHandler):
    def post(self):
        taskboardName = self.request.get('taskBoarddata')
        email = self.request.get('email')
        unique = taskboardName+""+email
        taskTitleName = self.request.get('Assign_Email')
        select_task_owner = self.request.get('select_task_owner')
        taskdata = ndb.Key('taskdata', unique).get()
        for i in range(0,len(taskdata.Title)):
            if taskdata.Title[i] == taskTitleName:
                taskdata.Task_assigned[i] = select_task_owner
                taskdata.put()
                self.redirect('/invite?taskBoarddata='+taskboardName+'&email='+email)

app = webapp2.WSGIApplication([
    ('/AssignValue',AssignValue)
], debug=True)
