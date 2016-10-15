import flask
import algo

app = flask.Flask(__name__)

@app.route("/")
def hello():
    return "OK"

@app.route("/emotion", methods=['POST'])
def emotion():
    content = flask.request.get_json(silent=True)
    print(content)
    result = algo.get_final_info(content['x_min'], content['x_max'],
    content['y_min'], content['y_max'], content['current_ts'],
    content['delta_t'], content['tags_considered'])
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
