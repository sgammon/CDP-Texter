from google.appengine.ext import db


class ModelMixin(object):
    __metaclass__ = db.PropertiedClass

    @classmethod
    def kind(self):
        """Need to implement this because it is called by PropertiedClass
        to register the kind name in _kind_map. We just return a dummy name.
        """
        return '__model_mixin__'

class AuditMixin(ModelMixin):

    modifiedBy = db.UserProperty(auto_current_user=True)
    createdBy = db.UserProperty(auto_current_user_add=True)
    modifiedAt = db.DateTimeProperty(auto_now=True)
    createdAt = db.DateTimeProperty(auto_now_add=True)


class List(db.Model, AuditMixin):
    
    ## key_name = short name of list
    name = db.StringProperty()
    description = db.TextProperty()


class ListMember(db.Expando, AuditMixin):
    
    ## parent = list
    ## key_name = phone number
    
    firstname = db.StringProperty()
    lastname = db.StringProperty()
    
    list_parent = db.ReferenceProperty(List, collection_name='members')
    phone_number = db.PhoneNumberProperty()
    
    
class TextJob(db.Model, AuditMixin):
    
    list_parent = db.ReferenceProperty(List, collection_name='jobs')
    text_subject = db.StringProperty()
    text_body = db.StringProperty()
    
    
class OutgoingText(db.Model):
    
    job = db.ReferenceProperty(TextJob, collection_name='texts')
    member = db.ReferenceProperty(ListMember, collection_name='texts')