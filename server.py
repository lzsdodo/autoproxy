#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, Flask, Response
from functools import wraps


# Config
NEED_AUTH = True
AUTH_USER = user
AUTH_PASSWD = passwd
PORT = port


def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


app = Flask(__name__)


@app.route('/status/', methods=['GET'])
def status():
    act = request.args.get('act')
    if act == 'change':
        with open('status.txt', 'w') as f:
            f.write('True')
        return 'Done'
    elif act == 'receive':
        with open('status.txt', 'w') as f:
            f.write('False')
        return 'Done'
    elif act:
        return 'Invalid action.'
    else:
        with open('status.txt', 'r') as f:
            status = f.read()
        return status


def check_auth(user, passwd):
    return user == AUTH_USER and passwd == AUTH_PASSWD \
        if NEED_AUTH else True

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/proxy/', methods=['GET'])
@requires_auth
def proxy():
    act = request.args.get('act')
    if act == 'set':
        ip = request.remote_addr
        with open('proxy.txt', 'w') as f:
            f.write('{}:{}'.format(ip, PORT))
        return 'Done'
    elif act:
        return 'Invalid action.'
    else:
        with open('proxy.txt', 'r') as f:
            proxy = f.read()
        return proxy


if __name__ == '__main__':
    from os import path
    from os import chdir
    fpath, fname = path.split(path.abspath(__file__))
    chdir(fpath)
    
    with open('status.txt', 'w') as f:
        f.write('False')
    with open('proxy.txt', 'w') as f:
        f.write('0.0.0.0:{}'.format(PORT))
    
    app.run(host='0.0.0.0')
