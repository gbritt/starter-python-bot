import json
import logging
import re
import NLTK_implement

logger = logging.getLogger(__name__)
'''
def set_glob_convostarted():

    self.conversation_started = True   # Needed to modify global copy of globvar
def set_convo_step():
    self.convo_step = "A"
    '''
'''
set_convo_step();
set_glob_convostarted();
'''


class RtmEventHandler(object):
    def _setglobvar(self):
        global convo_step
        global conversation_started
        convo_step = '1'
        conversation_started = 'False'


    def __init__(self, slack_clients, msg_writer, NLTK):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):
        exists = 'conversation_started' in locals() or 'conversation_started' in globals()

        if exists == False:
            self._setglobvar()
        else:
            if 'type' in event:
                self._handle_by_type(event['type'], event)
    def checkNLP(self,event):
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):
            msg_txt = event['text']
            tokenize, pos = NLTK_implementself.recieve_text(msg_txt)



    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        global conversation_started
        global convo_step
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
        global conversation_started
        global convo_step
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):
            msg_txt = event['text']

            if  conversation_started == 'False' and self.clients.is_bot_mention(msg_txt):
                # e.g. user typed: "@pybot tell me a joke!"
                if 'help' in msg_txt:
                    self.msg_writer.write_help_message(event['channel'])
                elif re.search('hi|hey|hello|howdy', msg_txt):
                    self.msg_writer.write_greeting(event['channel'], event['user'])
                    self.msg_writer.write_convo1(event['channel'], event['user'])
                    conversation_started = 'True'
                    convo_step = '2'
                    self.msg_writer.write_history(event['channel'], event['user'])
                    tokenize, pos = NLTK_implementself.recieve_text(msg_txt)
                    self.msg_write.write_NLP(event['channel'], event['user'], tokenize, pos)
                elif 'joke' in msg_txt:
                    self.msg_writer.write_joke(event['channel'])
                elif 'attachment' in msg_txt:
                    self.msg_writer.demo_attachment(event['channel'])
                elif 'echo' in msg_txt:
                    self.msg_writer.send_message(event['channel'], msg_txt)
                else:
                    self.msg_writer.write_prompt(event['channel'])

            elif conversation_started == 'True' and self.clients.is_bot_mention(msg_txt):
                if 'test' in msg_txt:
                    self.msg_writer.write_convo2(event['channel'], event['user'])
                    convo_step = '1'
                if convo_step == '2' and re.search('Yes|Yeah|Yup|mhm|mhmm|yessir|yessm|yes mam|yes|yeah|yar|yuo|yul|ok', msg_txt):
                    self.msg_writer.write_convo2_1(event['channel'], event['user'])
                    self.msg_writer.write_convo2_2(event['channel'], event['user'])
                    convo_step = '3'

                elif convo_step == '2' and re.search('no|No|NO|Nah|nah|nope|never', msg_txt):
                    self.msg_writer.write_convo2_neg(event['channel'], event['user'])
                    convo_step = '1'
                    conversation_started = 'False'
                elif convo_step == '3' and re.search('Yes|Yeah|yes|yeah|yup|Yup|mhm|mhmm|yessir|yessm|yes mam|yar|yuo|yul|ok', msg_txt):
                    self.msg_writer.write_convo3(event['channel'], event['user'])
                    convo_step = '4'


                elif convo_step == '3' and re.search('no|No|NO|Nah|nah|nope|never', msg_txt):
                    self.msg_writer.write_convo3_neg(event['channel'], event['user'])
                    convo_step = '1'
                    conversation_started = 'False'
                elif convo_step == '4' and re.search('Yes|Yeah|yes|yeah|yup|Yup|mhm|mhmm|yessir|yessm|yes mam|yar|yuo|yul|ok', msg_txt):
                    self.msg_writer.write_convo4(event['channel'], event['user'])
                    convo_step = '5'

                elif convo_step == '4' and re.search('no|No|NO|Nah|nah|nope|never', msg_txt):
                    self.msg_writer.write_convo4_neg(event['channel'], event['user'])
                    convo_step = '1'
                    conversation_started = 'False'

                elif convo_step == '5' and re.search('Yes|Yeah|yes|yeah|yup|Yup|mhm|mhmm|yessir|yessm|yes mam|yar|yuo|yul|ok', msg_txt):
                    self.msg_writer.write_convo5(event['channel'], event['user'])
                    convo_step = '1'
                    conversation_started = 'False'
                elif convo_step == '5' and re.search('no|No|NO|Nah|nah|nope|never', msg_txt):
                    self.msg_writer.write_convo5_neg(event['channel'], event['user'])
                    convo_step = '1'
                    conversation_started = 'False'
                else:
                    self.msg_writer.write_prompt(event['channel'])
