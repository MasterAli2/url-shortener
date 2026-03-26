from django.conf import settings

def global_template_vars(request):
    return {
        'APP_NAME':settings.APP_NAME
    }