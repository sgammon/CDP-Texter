# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE.txt for more details.
"""
from tipfy import Rule


def get_rules(app):
    """Returns a list of URL rules for the Hello, World! application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        
        ## Frontend URLs
        Rule('/', endpoint='list-groups', handler='apps.cdptexter.handlers.list.ListGroups'),
        Rule('/list/create', endpoint='list-create', handler='apps.cdptexter.handlers.list.ListCreate'),
        Rule('/list/<string:key>', endpoint='list-view', handler='apps.cdptexter.handlers.list.ListView'),
        Rule('/list/<string:key>/add', endpoint='list-add', handler='apps.cdptexter.handlers.list.ListAdd'),
        Rule('/list/<string:key>/send', endpoint='list-send', handler='apps.cdptexter.handlers.list.Send'),   
        Rule('/list/<string:key>/delete', endpoint='list-delete', handler='apps.cdptexter.handlers.list.Delete'),
        Rule('/list/<string:list_p>/entry/<string:entry>', endpoint='entry-view', handler='apps.cdptexter.handlers.entry.View'),
        Rule('/list/<string:list_p>/entry/<string:entry>/delete', endpoint='entry-delete', handler='apps.cdptexter.handlers.entry.Delete'),
        
        ## Workers
        Rule('/_worker/sms', endpoint='sms-worker', handler='apps.cdptexter.handlers.workers.SendSMS')
        
    ]

    return rules
