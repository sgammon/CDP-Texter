from . import get_list_form, get_entry_form, get_sms_form
from tipfy import RequestHandler, redirect_to, url_for
from tipfy.ext.jinja2 import Jinja2Mixin

from wtforms.ext.appengine.db import model_form

from tipfy.ext.wtforms import fields

from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

from apps.cdptexter.models import List, ListMember


class ListGroups(RequestHandler, Jinja2Mixin):
    
    def get(self):

        offset = int(self.request.args.get('offset', '0'))
        limit = int(self.request.args.get('limit', '20'))
        
        l = List.all().fetch(limit, offset)
        
        if len(l) == 0:
            l = False
        
        return self.render_response('list/list.html', data=l, title='Lists', next_limit=limit+20, next_offset=limit, prev_offset=offset-20)
        

class ListCreate(RequestHandler, Jinja2Mixin):
    
    def get(self):
        
        form = get_list_form(self.request)
        
        return self.render_response('list/create.html', form=form, title='Create List')
        
    def post(self):

        form = get_list_form(self.request)
        
        if form.validate():
            l = List(key_name=str(form.name.data).lower().replace(' ','-'), name=form.name.data, description=form.description.data).put()
            
            offset = 0
            limit = 20
            l = List.all().fetch(limit, offset)
            
            return self.render_response('list/list.html', data=l, title='Lists', flash='List successfully created.')
            
        else:
            return Response('<b>Form could not be validated. :(</b>')
        

class ListView(RequestHandler, Jinja2Mixin):
    
    def get(self, key):
        
        entry = db.get(db.Key(key))
        
        offset = int(self.request.args.get('offset', '0'))
        limit = int(self.request.args.get('limit', '20'))
        
        if hasattr(entry, 'members') and getattr(entry, 'members').count() > 0:
            has_members = True
        else:
            has_members = False
        
        return self.render_response('list/view.html', form=get_list_form(self.request, entry), title='View List', list=entry, has_members=has_members)
        
    def post(self, key):

        entry = db.get(db.Key(key))
        form = get_list_form(self.request, entry)
        
        if form.validate():
            entry.name = form.name.data
            entry.description = form.description.data
            
            entry.put()
            
            offset = 0
            limit = 20
        
            l = List.all().fetch(limit, offset)

            return self.render_response('list/list.html', data=l, title='Lists', flash='List successfully saved.')
            
        else:
            return Response('<b>Form could not be validated. :(</b>')
            
            
class Delete(RequestHandler, Jinja2Mixin):
    
    def get(self, key):
        
        key = db.Key(key)
        return self.render_response('list/delete.html', key=key)
        
    def post(self, key):
        
        key = db.Key(key)
        db.delete(key)
        
        offset = 0
        limit = 20
        l = List.all().fetch(limit, offset)
        
        return self.render_response('list/list.html', data=l, title='Lists', flash='List successfully deleted.')
        
        
class ListAdd(RequestHandler, Jinja2Mixin):
    
    def get(self, key):
        
        form = get_entry_form(self.request)
        list_p = db.get(db.Key(key))
        
        if self.request.args.get('addMore', False) == 'true':
            form.add_another = True
        else:
            form.add_another = False
        
        return self.render_response('entry/add.html', form=form, title='Add to List', list=list_p)
        
    def post(self, key):

        form = get_entry_form(self.request)
        
        if form.validate():

            list_p = db.Key(key)

            l = ListMember(list_p, key_name=str(form.phone_number.data), list_parent=list_p, firstname=str(form.firstname.data), lastname=str(form.lastname.data), phone_number=str(form.phone_number.data)).put()
            
            if form.add_another.data == True:
                return redirect_to('list-add', key=str(list_p), flash='Member added successfully.', addMore='true')
            else:            
                
                return redirect_to('list-view', key=str(list_p), flash='Member added successfully.')
            
        else:
            return Response('<b>Form could not be validated. :(</b>')        
            
            
class Send(RequestHandler, Jinja2Mixin):
    

    def get(self, key):

        list_p = db.get(db.Key(key))
        form = get_sms_form(self.request)
        
        return self.render_response('list/send.html', list=list_p, form=form)
        
        
    def post(self, key):

        list_p = db.get(db.Key(key))
        form = get_sms_form(self.request)
        
        if form.validate():
            
            message = form.message.data
            
            tasks = []
            status = []
            for item in list_p.members:
                tasks.append(taskqueue.Task(name=str(item.key()),url='/_worker/sms', method='POST', params={'message':message, 'list':str(list_p.key()), 'number': str(item.key().name())}))
                status.append({'list':str(list_p.key().name()), 'number':str(item.key().name())})
            
            q = taskqueue.Queue(name='outgoing-sms')
            tasks = q.add(tasks)
            
            return self.render_response('list/send-result.html', list=list_p, tasks=tasks, status=status)