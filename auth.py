from functools import wraps
from flask import request, Response
import hashlib


def format_credentials(username,password):
    return f"{username}:{hashlib.md5(password.encode()).hexdigest()}"


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    credentials =  format_credentials(username,password)

    with open('credentials.txt','r') as handler:        
        for line in handler.readlines():
            line = line[:-1]
            if line == credentials:
                return True
    return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated