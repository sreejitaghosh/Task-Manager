from google.appengine.ext import ndb

class taskdata(ndb.Model):
    Title = ndb.StringProperty(repeated = True)
    Due_Date = ndb.StringProperty(repeated = True)
    Task_Completion = ndb.StringProperty(repeated = True)
    Task_assigned = ndb.StringProperty(repeated = True)
    Date = ndb.StringProperty(repeated = True)
    Time = ndb.StringProperty(repeated = True)
