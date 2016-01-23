from bottle import default_app, route, hook, request

app = default_app()

@hook('before_request')
def strip_path():
    # Remove trailing slashes from all request before routing the request
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

@route('/hello')
def hello():
    return "Hello World!"

@route('')
def mainpage():
    return "Welcome"