import flask

app = flask.Flask(__name__)

@app.route("/")
def hello():
    return "OK"

@app.route("/emotion")
def emotion():
    print(flask.request.data)
    return flask.jsonify({"gaoce": "1"})

@app.route("/tags")
def tags():
    return flask.jsonify({"gaoce": "1"})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run()
