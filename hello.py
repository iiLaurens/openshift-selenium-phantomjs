from bottle import default_app

app = default_app()

@route('/hello')
def hello():
    return "Hello World!"

@route('/')
@route('')
def mainpage():
    return "Welcome"

#run(app, server='gevent')