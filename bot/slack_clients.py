
import logging
import re
import time

from slacker import Slacker
from slackclient import SlackClient

logger = logging.getLogger(__name__)


class SlackClients(object):
    def __init__(self, token):
        self.token = token

        # Slacker is a Slack Web API Client
        self.web = Slacker(token)

        # SlackClient is a Slack Websocket RTM API Client
        self.rtm = SlackClient(token)

    def bot_user_id(self):
        return self.rtm.server.login_data['self']['id']

    def is_message_from_me(self, user):
        return user == self.rtm.server.login_data['self']['id']

    def is_bot_mention(self, message):
        bot_user_name = self.rtm.server.login_data['self']['id']
        if re.search("@{}".format(bot_user_name), message):
            return True
        else:
            return False

    def send_user_typing_pause(self, channel_id, sleep_time=3.0):
        user_typing_json = {"type": "typing", "channel": channel_id}
        self.rtm.server.send_to_websocket(user_typing_json)
        time.sleep(sleep_time)
    def get_chat_history(self,channel_id, pageSize = 100):
        '''
        channels = slack.channels.list().body['channels']
        messages = []
        lastTimestamp = None
        response = channel.history(
        channel = channel_id
        latest = lastTimestamp
        oldest = 0
        count = pageSize
        ).body
        messages.extend(response['messages'])
        return messages
        '''
        a = self.rtm.api_call('channels.history', channel = channel_id)

        return a
        #print self.rtm.api_call("chat.post_Message", as_user = "true:", channel = channel_id, text = test)
        #self.trm.server.send_to_websocket
