import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class DeleteTask(webapp2.RequestHandler):
    def post(self):
        taskboardName = self.request.get('taskBoarddata')
        email = self.request.get('email')
        unique = taskboardName+""+email
        taskTitleName = self.request.get('DeleteButton')
        taskdata = ndb.Key('taskdata', unique).get()
        if len(taskdata.Title) > 1:
            for i in range(0,len(taskdata.Title)):
                if taskdata.Title[i] == taskTitleName:
                    del taskdata.Title[i]
                    del taskdata.Due_Date[i]
                    del taskdata.Task_Completion[i]
                    del taskdata.Date[i]
                    del taskdata.Time[i]
                    taskdata.put()
                    self.redirect('/invite?taskBoarddata='+taskboardName+'&email='+email)
        else:
            taskdata.key.delete()
            self.redirect('/invite?taskBoarddata='+taskboardName+'&email='+email)

app = webapp2.WSGIApplication([
    ('/deleteTask',DeleteTask)
], debug=True)
