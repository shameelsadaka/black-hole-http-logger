from flask import Flask, request, render_template
import json
import pickle
import time
from datetime import datetime
import sys
import getpass
import hashlib
from auth import requires_auth , format_credentials

app = Flask(__name__)

FILE_NAME = "requests.log"

LOGS = []

MAX_LOG_LENGTH = 50
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']



@app.template_filter()
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y %B %d %H:%M:%S" )

@app.context_processor
def num_of_logs():
    return dict(num = len(LOGS))


@app.route('/dashboard')
@app.route('/dashboard/')
@requires_auth
def dashboard():
    return render_template('dashboard.html', logs=LOGS[::-1])  


@app.route('/log/<path:path>', methods=HTTP_METHODS)
def logger(path):
    LOGS.append({
        'method': request.method,
        'path': path,
        'time': int(time.time()),
        'ip': request.remote_addr,
        'headers': request.headers,
        'body': str(request.get_data())
    })
    while len(LOGS) > MAX_LOG_LENGTH:
        LOGS.pop(0) 
    
    return "OK"

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "createsuperuser":
        username = input("Enter admin email: ")


        password = getpass.getpass("Enter Password: ")
        confirm_password = getpass.getpass("Enter Password Again: ")

        if password != confirm_password:
            print("Passwords does't match")
            exit()

        with open('credentials.txt','a') as handler:
            handler.write(format_credentials(username,password)+"\n")

        print("Created")

    else:
        app.run(debug=True, host='0.0.0.0')
