from google.appengine.ext import ndb
from taskdata import taskdata

class taskBoarddata(ndb.Model):
    taskBoarddata = ndb.StringProperty()
    email_address = ndb.StringProperty(repeated=True)
    owner = ndb.StringProperty()
