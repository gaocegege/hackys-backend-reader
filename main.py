import flask
import algo

app = flask.Flask(__name__)

@app.route("/")
def hello():
    return "OK"

@app.route("/emotion")
def emotion():
    result = algo.get_final_info(flask.request.data['x_min'], flask.request.data['x_max'],
    flask.request.data['y_min'], flask.request.data['y_max'], flask.request.data['current_ts'],
    flask.request.data['delta_t'], flask.request.data['tags_considered'])
    print(result)
    return flask.jsonify(result)

@app.route("/tags")
def tags():
    result = algo.get_all_tags()
    return flask.jsonify(result)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(port=8089, host="0.0.0.0")
