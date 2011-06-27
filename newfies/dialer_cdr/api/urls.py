from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from piston.doc import documentation_view
from handlers import callrequestHandler, testcallHandler, \
answercallHandler, hangupcallHandler
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
#import custom_xml_emitter
from common.custom_xml_emitter import *
from settings import ALLOWED_IP_LIST


class IpAuthentication(object):
    """
    IP Authentication handler
    """
    def __init__(self, auth_func=authenticate, realm='API'):
        self.auth_func = auth_func
        self.realm = realm

    def is_authenticated(self, request):
        try:
            ALLOWED_IP_LIST.index(request.META['REMOTE_ADDR'])
            return True
        except:
            return False

    def challenge(self):
        resp = HttpResponse("Not Authorized")
        resp.status_code = 401
        return resp

auth = HttpBasicAuthentication(realm='Newfies Application')
auth_ip = IpAuthentication()

callrequest_handler = Resource(callrequestHandler, authentication=auth)
answercall_handler = Resource(answercallHandler, authentication=auth_ip)
hangupcall_handler = Resource(hangupcallHandler, authentication=auth_ip)
testcall_handler = Resource(testcallHandler, authentication=auth_ip)


urlpatterns = patterns('',

    url(r'^callrequest[/]$', callrequest_handler),
    url(r'^callrequest/(?P<callrequest_id>[^/]+)', callrequest_handler),

    url(r'^answercall[/]$', answercall_handler,
                                    {'emitter_format': 'custom_xml'}),
    url(r'^hangupcall[/]$', hangupcall_handler,
                                    {'emitter_format': 'custom_xml'}),
    
    url(r'^testcall[/]$', testcall_handler),

    # automated documentation
    url(r'^doc[/]$', documentation_view),
)
