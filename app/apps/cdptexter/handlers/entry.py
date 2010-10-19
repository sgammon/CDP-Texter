from . import get_list_form, get_entry_form

from tipfy import RequestHandler, redirect_to

from tipfy.ext.jinja2 import Jinja2Mixin

from google.appengine.ext import db
from apps.cdptexter.models import ListMember
from wtforms.ext.appengine.db import model_form


class View(RequestHandler, Jinja2Mixin):


    def get(self, list_p, entry):

        entry = db.get(db.Key(entry))
        return self.render_response('entry/view.html', form=get_entry_form(self.request, entry), title='View Entry', key=entry, list=db.get(db.Key(list_p)))
        
        
    def post(self, list_p, entry):

        entry = db.get(db.Key(entry))
        list_p = db.get(db.Key(list_p))
        form = get_entry_form(self.request)
        
        if form.validate():
            
            if entry.phone_number != form.phone_number.data:
                db.delete(entry)
                entry = ListMember(list_p, key_name=form.phone_number.data, phone_number=form.phone_number.data)
                
            entry.firstname = form.firstname.data
            entry.lastname = form.lastname.data
            
            entry.put()
            
            return redirect_to('list-view', key=str(list_p.key()), flash='Member successfully saved.')
                
    
    
class Delete(RequestHandler, Jinja2Mixin):

    def get(self, list_p, entry):
        
        entry = db.Key(entry)
        return self.render_response('entry/delete.html', key=entry, title='Delete Entry')
        
        
    def post(self, list_p, entry):
        
        key = db.get(db.Key(entry))
        parent = key.parent()
        
        key.delete()
        
        return self.render_response('list/view.html', flash='Member entry deleted successfully.', list=parent, title='View List')