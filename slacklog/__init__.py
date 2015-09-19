from collections import deque
from flask import Flask
from flask.ext.redis import FlaskRedis
from flask_sockets import Sockets
from slacker import Slacker

app = Flask(__name__)
app.config.from_object('config')

redis_store = FlaskRedis(app)
sockets = Sockets(app)
messages = deque(maxlen=25)
slack_users = {}
slack_channels = {}

slack = Slacker(app.config['SLACK_API_TOKEN'])

users_response = slack.users.list()
if users_response.body['ok']:
    users = users_response.body['members']
    for user in users:
        slack_users[user['id']] = user

channels_response = slack.channels.list()
if channels_response.body['ok']:
    channels = channels_response.body['channels']
    for channel in channels:
        slack_channels[channel['id']] = channel

from slacklog.ws import Backend
backend = Backend()
backend.start()

from slacklog import views