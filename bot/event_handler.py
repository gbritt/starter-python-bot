import json
import logging
import re

logger = logging.getLogger(__name__)
def set_glob_convostarted():
    global conversation_started    # Needed to modify global copy of globvar
def set_convo_step():
    global convo_step
set_convo_step();
set_glob_convostarted();
class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)


    def _handle_by_type(self, event_type):
        # See https://api.slack.com/rtm for a full list of events

        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself, and from non-users (eg. webhooks)
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):
            msg_txt = event['text']
            if  conversation_started == False:

            #if self.clients.is_bot_mention(msg_txt):
                # e.g. user typed: "@pybot tell me a joke!"
                if 'help' in msg_txt:
                    self.msg_writer.write_help_message(event['channel'])
                elif re.search('hi|hey|hello|howdy', msg_txt):
                    self.msg_writer.write_greeting(event['channel'], event['user'])
                    self.msg_write.write_convo1(event['channel'])
                    conversation_started = True

                elif 'joke' in msg_txt:
                    self.msg_writer.write_joke(event['channel'])
                elif 'attachment' in msg_txt:
                    self.msg_writer.demo_attachment(event['channel'])
                elif 'echo' in msg_txt:
                    self.msg_writer.send_message(event['channel'], msg_txt)
                else:
                    self.msg_writer.write_prompt(event['channel'])
            elif conversation_started == True:
                if convo_step == 'AA' and re.search('Yes/Yeah/Yup/mhm/mhmm/yessir/yessm/yes mam/yar/yuo/yul/ok', msg_test):
                    self.msg_writer.write_convo2(event['channel'])
                    convo_step = 'B'
                elif convo_step == 'AA' and re.seach('no/No/NO/Nah/nah/nope/never', msg_test):
                    self.msg_writer.write_convo3_neg(event['channel'])
                    convo_step = 'AA'
                    conversation_started = False
                elif convo_step == 'B' and re.search('Yes/Yeah/Yup/mhm/mhmm/yessir/yessm/yes mam/yar/yuo/yul/ok', msg_test):
                    self.msg_writer.write_convo3(event['channel'])
                    convo_step = 'AA'
                    conversation_started = False
