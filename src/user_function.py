import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from server import defaultHandler

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

USERDATASTORE = []

#APP route
def workspace_reset(email, password, name_first, name_last):
    global DATASTORE
    USERDATASTORE = []
    return None


# Zach user prof
@APP.route("/user/profile/sethandle", method=["PUT"])
def user_handle():
        global DATASTORE
        data = request.get_json()
        token = data['token']
        # Validate token first
        if (checktoken(token) != 1) {
            raise InputError
        }
        set_handle = data['handle_str']
        if (len(set_handle) <= 2 and >= 20) and checkhandle(DATASTORE, set_handle) == 1:
            raise InputError
        DATASTORE['handle_str'] = set_handle
        return dumps({})


# input token
def checkhandle( USERDATASTORE , str given_handle):
    for x in USERDATASTORE['User']['handle_string']:
        if x == given_handle:
           return InputError
        else:
            return 1

def checktoken(USERDATASTORE, str given_token):
    for x in USERDATASTORE['User']['token']:
        if x == given_token:
            return 1
        else:
            print("User does not exist")
            return None
