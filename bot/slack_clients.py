
import logging
import re
import time
import json
import argparse
import os

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
    def upload_file(self,file,channel_id):
        #self.rtm.api_call('')
        self.web.files.upload(file, channels = self.web.channels.get_channel_id('channel_id'))

    def upload(self, file, channel)
        token = self.token
        options = {
        token: @team.bot[token],
        file: File.new("./tmp/composed/#{file.timestamp}", 'rb'),
        filename: "composed_" + file.name,
        title: "Composed " + file.title,
        channels: channel
        }

  res = RestClient.post 'https://slack.com/api/files.upload', options
  # Return the uploaded file's ID
  JSON.parse(res.body)["file"]["id"]
end
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
        #history = self.rtm.api_call('channels.history', channel = channel_id)
        channelHistory = self.rtm.api_call('channels.history', channel = channel_id)

        '''
        with open(channelHistory, 'r') as handle:
            parsed = json.load(handle)
        '''


        '''
        with open(fileName, 'w') as outFile:
            print("writing {0} records to {1}".format(len(messages), fileName))
            json.dump({'channel_info': channelInfo, 'messages': messages }, outFile, indent=4)

        channels = slack.channels.list().body['channels']
        return (channel['name'])
        #print self.rtm.api_call("chat.post_Message", as_user = "true:", #channel = channel_id, text = test)
        #self.trm.server.send_to_websocket
        '''
