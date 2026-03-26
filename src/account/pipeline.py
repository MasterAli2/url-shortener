from social_core.exceptions import AuthException

def deny_signup(backend, uid, user=None, *args, **kwargs):
    if user is None:
        raise AuthException(backend, 'No Account found for this Discord account.')