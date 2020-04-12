from google.appengine.ext import ndb

class taskdata(ndb.Model):
    Title = ndb.StringProperty()
    Due_Date = ndb.DateTimeProperty()
    Task_Completion = ndb.StringProperty()
