import os
from flask import Flask, request, send_file, make_response
from datetime import datetime
from flask_socketio import SocketIO
from secrets import token_urlsafe

app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe(20)
socketio = SocketIO(app, cors_allowed_origins="*")

def get_event():
    return {
        'method': request.method,
        'path': request.path,
        'form': request.form,
        'cookies': request.cookies
    }

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        event = get_event() | {
                 'response-headers': {
                     'Access-Control-Allow-Origin': request.origin,
                     'Access-Control-Allow-Methods': request.headers.get('Access-Control-Request-Method'),
                     'Access-Control-Allow-Headers': 'authorization'
                 },
                 'incoming-headers': { k: v for k,v in request.headers.items() if k.startswith("Access")}
        }
        if request.path.endswith("-cred"):
            event['response-headers']['Access-Control-Allow-Credentials'] =  'true'
        res = make_response()
        res.headers.extend(event['response-headers'])
        socketio.emit('server', event)
        return res

@app.route('/')
def hello():
    socketio.emit('server', get_event())
    return 'API Server Running'


@app.route('/set-cookie',  methods = ['GET', 'POST'])
def setcookie():
    event = get_event() | {
        'returned-cookie': {"name": "snickerdoodle", "value": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    }
    socketio.emit('server', event)
    resp = make_response("I just gave you a cookie")
    resp.set_cookie(event['returned-cookie']['name'], event['returned-cookie']['value'], samesite="none", secure=True)
    return resp

@app.route('/drop-cookie',  methods = ['GET', 'POST'])
def dropcookie():
    event = get_event() | {
        'returned-cookie': {"name": "snickerdoodle", "value": "-deleted-"}
    }
    socketio.emit('server', event)
    resp = make_response("I just gave you a cookie")
    resp.set_cookie(event['returned-cookie']['name'], event['returned-cookie']['value'], samesite="none", secure=True, expires=1)
    return resp


@app.route('/action',  methods = ['POST'])
def action():
    event = get_event()
    return process_action(event)


@app.route('/action-cors',  methods = ['POST'])
def action_cors():
    event = get_event() | {
        'response-headers' : {
            'Access-Control-Allow-Origin': request.origin
        }
    }
    return process_action(event)


@app.route('/action-cors-cred',  methods = ['POST'])
def action_cors_cred():
    event = get_event() | {
        'response-headers' : {
            'Access-Control-Allow-Origin': request.origin,
            'Access-Control-Allow-Credentials': 'true'
        }
    }
    return process_action(event)

@app.route('/action-cors-all-cred',  methods = ['POST'])
def action_cors_all_cred():
    event = get_event() | {
        'response-headers' : {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true'
        }
    }
    return process_action(event)

def process_action(event):
    message = "Thank you for your data: " + ", ".join([f"{k}: {v}" for k, v in request.form.items()])
    event['body'] = message
    socketio.emit('server', event)
    resp = make_response(message)
    resp.headers.extend(event.get('response-headers', {}))
    return resp

@app.route('/image')
def image():
    event = get_event()
    socketio.emit('server', event)
    resp = make_response(send_file("generate.jpeg"))
    resp.headers.extend(event.get('response-headers', {}))
    return resp

@app.route('/image-cors')
def image_cors():
    event = get_event() | {
        'response-headers' : {
            'Access-Control-Allow-Origin': '*',
        }
    }
    socketio.emit('server', event)
    resp = make_response(send_file("generate.jpeg"))
    resp.headers.extend(event.get('response-headers', {}))
    return resp


if __name__ == '__main__':
    path_cert = "certs/site.crt"
    path_key = "certs/site.key"
    if (not os.path.isfile(path_cert) or not os.path.isfile(path_key)):
        raise RuntimeError(f"Missing 1 or more required files: {path_cert}, {path_key}")
    socketio.run(app, use_reloader=False, log_output=True, ssl_context=(path_cert, path_key))
