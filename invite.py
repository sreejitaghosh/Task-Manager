import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from taskBoarddata import taskBoarddata
from taskdata import taskdata

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
        length_task_data = 0

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
        assigned_users = taskboard_data.email_address
        task_data = ndb.Key('taskdata',taskBoard_key).get()
        if task_data != None:
            length_task_data = len(task_data.Title)

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'available_email_id' : available_email_id,
             'taskboard_data' : taskboard_data,
             'task_data' : task_data,
             'length_task_data' : length_task_data,
             'assigned_users' : assigned_users
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
        option = self.request.get('submit')
        select_to_remove_email_id = self.request.get('select_to_remove_email_id')

        if option == 'Invite':
            if taskBoard_a.owner == user.email():
                section = False
                if user_select_email != "":
                    new_myuser = ndb.Key('MyUser',user_select_email).get()
                    if new_myuser != None:
                        call = new_myuser.taskboard
                        i = 0
                        while i < len(call):
                            if call[i] == all_call:
                                section = True
                                break
                            else:
                                i = i + 1
                    if section == True:
                        self.redirect('/taskBoard')
                    else:
                        new_myuser.taskboard.append(all_call)
                        new_myuser.put()
                        taskBoard_a.email_address.append(user_select_email)
                        taskBoard_a.put()
                        self.redirect('/invite?taskBoarddata='+call_tb+'&email='+call_user)
                else:
                    self.redirect('/taskBoard')
            else:
                self.redirect('/taskBoard')

        elif option == 'Remove':
            if taskBoard_a.owner == user.email():
                if select_to_remove_email_id != "":
                    new_myuser = ndb.Key('MyUser',select_to_remove_email_id).get()
                    taskData = ndb.Key('taskdata',all_call).get()
                    if taskData != None:
                        k = 0
                        while k in range(0,len(taskData.Title)):
                            if taskData.Task_assigned[k] == select_to_remove_email_id:
                                taskData.Task_assigned[k] = "Not Assigned"
                            else:
                                k = k + 1
                    j = 0
                    while j in range(0,len(taskBoard_a.email_address)):
                        if taskBoard_a.email_address[j] == select_to_remove_email_id:
                            del taskBoard_a.email_address[j]
                            break
                        else:
                            j = j + 1
                    i = 0
                    while i in range(0,len(new_myuser.taskboard)):
                        if new_myuser.taskboard[i] == all_call:
                            del new_myuser.taskboard[i]
                            taskData.put()
                            taskBoard_a.put()
                            new_myuser.put()
                            break
                        else:
                            i = i + 1
                    self.redirect('/invite?taskBoarddata='+call_tb+'&email='+call_user)
            else:
                self.redirect('/taskBoard')

        elif option == "Rename":
            tb_new = self.request.get('taskboard_NewName')
            check_exist = ndb.Key('taskBoarddata',tb_new+""+call_user).get()
            if check_exist == None:
                task_Old = ndb.Key('taskdata',all_call).get()
                if task_Old != None:
                    task_connect = taskdata(id=tb_new+""+call_user)
                    task_connect.Title = task_Old.Title
                    task_connect.Due_Date = task_Old.Due_Date
                    task_connect.Task_Completion = task_Old.Task_Completion
                    task_connect.Task_assigned = task_Old.Task_assigned
                    task_connect.Date = task_Old.Date
                    task_connect.Time = task_Old.Time
                    task_connect.put()
                    task_Old.key.delete()

                tb_Old = ndb.Key('taskBoarddata',all_call).get()
                tb_connect = taskBoarddata(id=tb_new+""+call_user)
                tb_connect.taskBoarddata = tb_new
                tb_connect.email_address = tb_Old.email_address
                email_id = tb_connect.email_address
                tb_connect.owner = tb_Old.owner

                i = 0
                while i in range(0,len(email_id)):
                    user_db = ndb.Key('MyUser',email_id[i]).get()
                    if user_db != None:
                        j = 0
                        while j in range(0,len(user_db.taskboard)):
                            if user_db.taskboard[j] == all_call:
                                user_db.taskboard[j] = tb_new+""+call_user
                                user_db.put()
                                j = j + 1
                            else:
                                j = j + 1
                        i = i + 1
                    else:
                        i = i + 1
                tb_connect.put()
                tb_Old.key.delete()
                self.redirect('/invite?taskBoarddata='+tb_new+'&email='+call_user)
            else:
                self.redirect('/taskBoard')

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
