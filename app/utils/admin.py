from flask import session, redirect
from functools import wraps

# operates similarly to the login required wrapper, only difference is that it's reserved for routes only admins can access
def admin_required():
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if session.get('loggedIn') == True and session.get('isAdmin') == True:
            return func(*args, **kwargs)
        return redirect('/home')
    
    return wrapped_function