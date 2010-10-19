from wtforms.ext.appengine.db import model_form
from apps.cdptexter.models import List, ListMember

from tipfy.ext.wtforms import Form, fields, validators

audit_params = ['modifiedBy','modifiedAt','createdBy','createdAt']


class ListForm(Form):

    name = fields.TextField('Name', validators=[validators.required()])
    description = fields.TextAreaField('Description', validators=[validators.required()])
    submit = fields.SubmitField()


class EntryForm(Form):

    firstname = fields.TextField('First Name', validators=[validators.optional()])
    lastname = fields.TextField('Last Name', validators=[validators.optional()])
    phone_number = fields.TextField('Phone Number', validators=[validators.required()])

    add_another = fields.BooleanField('Add another?', default=False)
    submit = fields.SubmitField()
    
    
class SMSForm(Form):
    
    message = fields.TextAreaField('Message', validators=[validators.required()])
    submit = fields.SubmitField()


def get_list_form(request, obj=None):
    
    global audit_params

    if obj is None:
        m = ListForm(request)
    else:
        m = ListForm(request, obj=obj)
        
    m.submit = fields.SubmitField()
        
    return m
    
    
def get_entry_form(request, obj=None):

    global audit_params
    
    if obj is None:
        m = EntryForm(request)
    else:
        m = EntryForm(request, obj=obj)

    m.submit = fields.SubmitField()
        
    return m
    
    
def get_sms_form(request):
    
    return SMSForm(request)