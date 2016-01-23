from bottle import Bottle

app = Bottle()

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/')
@app.route('')
def mainpage():
    return "Welcome"

#run(app, server='gevent')