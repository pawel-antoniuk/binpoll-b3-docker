from django.core.exceptions import PermissionDenied
from data_collector.views import AuthView
from django.http import HttpResponseForbidden

def cors_headers_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if 'Access-Control-Allow-Headers' in response:
                h = response['Access-Control-Allow-Headers']
                response['Access-Control-Allow-Headers'] = ','.join(h.split(',') + ['message-type'])
        return response
    return middleware


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        #raise PermissionDenied()
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if (hasattr(view_func, 'view_class') 
                and hasattr(view_func.view_class, 'auth') 
                and view_func.view_class.auth(request)):
            return None
        if 'auth' in request.session and request.session['auth']:
            return None
        return HttpResponseForbidden()
