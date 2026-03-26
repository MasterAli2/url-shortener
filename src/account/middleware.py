from social_core.exceptions import AuthAlreadyAssociated

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class SocialAuthSpecialExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response 
        
    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            messages.error(request, 'This account is already in use by another user.', extra_tags='AuthAlreadyAssociated')
            
            return redirect(reverse('account'))