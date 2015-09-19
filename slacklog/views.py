import gevent
import json

from flask import request, render_template, abort

from slacklog import app, messages, redis_store, sockets, backend
from slacklog.models import Message


@app.route("/")
def index():
    return render_template("index.html", messages=messages)

@app.route("/input", methods=["POST"])
def input_slack_message():
    msg = Message(timestamp=request.form['timestamp'],
                  service_id=request.form['service_id'],
                  channel_id=request.form['channel_id'],
                  team_domain=request.form['team_domain'],
                  text=request.form['text'],
                  token=request.form['token'],
                  user_name=request.form['user_name'],
                  team_id=request.form['team_id'],
                  user_id=request.form['user_id'],
                  channel_name=request.form['channel_name'])
    if msg.token == app.config['SLACK_INPUT_TOKEN']:
        msg.process()
        messages.append(msg)
        redis_store.publish(app.config['REDIS_CHAN'], json.dumps(msg.__dict__))
        return "ok"
    else:
        abort(403)

@sockets.route('/ws')
def ws_endpoint(ws):
    backend.register(ws)

    while not ws.closed:
        gevent.sleep()