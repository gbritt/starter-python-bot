# -*- coding: utf-8 -*-

import logging
import random
import sys

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
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations', 
                    'One bit of sage advice for grandparents — show up, shut up, and smile.', 'Let"s have a fireside chat','Their smiles are a delight and their enjoyment of life palpable.','Grandchildren are wonderfully insightful — one asked my wife why she always needs to be the boss. They have figured out that I like the golf channel and enjoy sitting with their grandfather commenting on various putting strokes.','It is much easier being a grandparent than a parent — trust me.','I have to admit that I frequently got graded as needs improvement as a parent. Yes, there was the time I forgot to pick up my son at school, and a time I put him on a sled in a snow storm attached to a dog and the dog took off across Valley Forge Park, and a time I forgot his duffel bag for a ski trip, and the time, well you get it.','This is a great moment. You are beginning a journey that will be life altering.', 'Fortunately, medicine is an egalitarian profession — hard work and grit are the currency.', 'Each of you has many assets that you should understand and maximize.','Has anyone here not faced adversity? Congratulations if you have not, but no doubt you will.','I"m being honest. I"m working with a third of what our Congress has promised','Enjoy the journey for surely yours will be special.', 'The refrain of this song from the 1959 Broadway musical, Fiorello, surely rings true today. Politics and poker, politics and poker.  Shuffle up the cards and find the joker',  'Talk Less, Smile More.','Where are the role models if our highest office - seekers are mud wrestling? ', 'Games of chance are not something we want to bet our future on.']
                
                  

        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

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
