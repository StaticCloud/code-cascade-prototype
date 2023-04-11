from flask import session, redirect
from functools import wraps

def login_required(func): # define our decorator function
    @wraps(func) # wrapper that preserves metadata of a decorated function
    def wrapped_function(*args, **kwargs): # defines the inner function
        if session.get('loggedIn') == True: # checks if the client making the request is logged in
            return func(*args, **kwargs) # execute the function if the user is logged in
        return redirect('/login') # otherwise, redirect to the login page
    
    return wrapped_function