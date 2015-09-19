import re

from slacklog import slack_users, slack_channels


class Message(object):
    def __init__(self,
                 timestamp,
                 service_id,
                 channel_id,
                 team_domain,
                 text,
                 token,
                 user_name,
                 team_id,
                 user_id,
                 channel_name):
         self.timestamp = timestamp
         self.service_id = service_id
         self.channel_id = channel_id
         self.team_domain = team_domain
         self.text = text
         self.token = token
         self.user_name = user_name
         self.team_id = team_id
         self.user_id = user_id
         self.channel_name = channel_name

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<%s>: %s" % (self.user_name, self.text)

    def process(self):
        if self.user_id in slack_users:
            user = slack_users[self.user_id]
            self.user_real_name = user['profile']['real_name']
            self.user_image = user['profile']['image_192']

        def process_line(m):
            if m.group(1) and m.group(1) == "@":
                if m.group(2) in slack_users:
                    user = slack_users[m.group(2)]
                    return "<a href='#'>@%s (%s)</a>" % (user['name'], user['real_name'])
            elif m.group(1) and m.group(1) == "#":
                if m.group(2) in slack_channels:
                    channel = slack_channels[m.group(2)]
                    return "<a href='#'>#%s</a>" % channel['name']
            else:
                return "<a href='%s'>%s</a>" % (m.group(2), m.group(2))

        self.text = re.sub("<(@|#)?(.*?)>", process_line, self.text)
        return