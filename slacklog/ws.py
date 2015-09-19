import gevent
from slacklog import app, redis_store


class Backend(object):
    def __init__(self):
        self.clients = list()
        self.pubsub = redis_store.pubsub()
        self.pubsub.subscribe(app.config['REDIS_CHAN'])

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                yield data

    def register(self, client):
        self.clients.append(client)

    def send(self, client, data):
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        gevent.spawn(self.run)