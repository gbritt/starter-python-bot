# -*- coding: utf-8 -*-

import logging
import random
import sys
import os
from slacker import Slacker
import json
import argparse
import os

logger = logging.getLogger(__name__)
#sys.setdefaultencoding("utf-8")



class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: %s to channel: %s' % (msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message(msg)

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}'.format(
            "I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:")
        self.send_message(channel_id, txt)


    def write_greeting(self, channel_id, user_id):

        with open('test.txt', 'r') as filestream:
            for line in filestream:
                greetings = line.split(",")


        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)
# Section for initial conversation between grossman and patient
    def write_history(self,channel_id,user_id): #doesn't working
        channelHistory = self.clients.get_chat_history(channel_id)


        fileName = 'convo.txt'

        #with open(fileName, 'w') as outFile:
            #outFile.write('test')

        with open(fileName, 'w') as outFile:
            json.dumps({'channel_history': channelHistory}, outFile, indent = 4)

        #self.clients.upload_file('test.txt', channel_id) #can probably dead with channel id better
        #self.send_message(channel_id, history)
    def write_convo1(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "Hello! This chatbot has been created to help you identify questions you want to ask your doctor, so you can get what you need from your appointment."
        self.send_message(channel_id, suggestion)
        self.clients.send_user_typing_pause(channel_id)
        question = "Are you Here for an appointment?"
        self.send_message(channel_id, question)
    def write_convo2_1(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "To start, have you thought about the most important question you want to ask your doctor? "
        self.send_message(channel_id, suggestion)

    def write_convo2_2(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "By the way, no personal information will be collected, and nothing typed here will be seen by a doctor. This purpose of this chat is to help you prepare for an appointment."
        self.send_message(channel_id, suggestion)

    def write_convo2_neg(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "Okay, have a great day!"
        self.send_message(channel_id, suggestion)

    def write_convo3(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "Terrific! You are on your way to making sure you have a productive appointment."
        self.send_message(channel_id, suggestion)
        self.clients.send_user_typing_pause(channel_id)
        suggestion2 = "Next, you should think about any prescriptions or refills that you want to ask about. This included medications, devices, and glasses."
        self.send_message(channel_id, suggestion2)
        self.clients.send_user_typing_pause(channel_id)
        suggestion3 = "Have you thought about it?"
        self.send_message(channel_id, suggestion3)
    def write_convo3_neg(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "Okay, thank you for learning more about this chatbot today! Have a good appointment!"
        self.send_message(channel_id, suggestion)

    def write_convo4(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "Nice! You are doing great"
        self.send_message(channel_id, suggestion)
        self.clients.send_user_typing_pause(channel_id)
        suggestion2 = "Next, do you have any sensitive or private topics that you want to ask your doctor about? The doctor's office is a safe space to ask questions."
        self.send_message(channel_id, suggestion2)
        self.clients.send_user_typing_pause(channel_id)
        suggestion3 = "Many patients find this difficult, but together you and your dcotor can take better care of your health if you share any relevant information."
        self.send_message(channel_id, suggestion3)
        self.clients.send_user_typing_pause(channel_id)
        suggestion4 = "Are you thinking about it? You are almost done!"
        self.send_message(channel_id, suggestion4)
    def write_convo4_neg(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "Okay, well think about it you dummy! Have a good appointment!"
        self.send_message(channel_id, suggestion)

    def write_convo5(self, channel_id, user_id):

        suggestion = "Cool!"
        self.send_message(channel_id, suggestion)
        self.clients.send_user_typing_pause(channel_id)
        suggestion2 = "Make sure to ask your doctor the 3 things you just throught about.  Remember 1: your most important question, 2: prescriptions you want to ask about, 3: sensitive or private topics you want to ask about.  Have a great day!"
        self.send_message(channel_id, suggestion2)

    def write_convo5_neg(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "Okay, well have a good appointment!"
        self.send_message(channel_id, suggestion)
    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)


    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')

    def text_attachment(self, channel_id, user_id):
        #this doesn't seem to work due to slack api bug
        channelHistory = self.clients.get_chat_history(channel_id)
        txt = "Hello! This is your chat log"
        attachment = {

            "title": "THi is a test",
            "text": channelHistory,
            "fallback": txt,
            "color": "#7CD197",
        }
        self.clients.web.files.upload('test.txt')
    def write_NLP(self, channel_id, user_id, tokenize, pos):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        tokenize = str(tokenize)
        self.send_message(channel_id, tokenize)
