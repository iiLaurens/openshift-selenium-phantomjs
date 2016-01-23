from bottle import default_app, route, hook, request

app = default_app()

@hook('before_request')
def strip_path():
    # Remove trailing slashes from all request before routing the request
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

@route('/hello')
def hello():
    for i in range(1,11):
        yield str(i)
        sleep(1)

@route('/')
def mainpage():
    return "Welcome"