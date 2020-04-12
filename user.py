from google.appengine.ext import ndb

class MyUser(ndb.Model):
    email_address = ndb.StringProperty()
    taskboard = ndb.StringProperty(repeated=True)
