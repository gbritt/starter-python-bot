import json

import requests
import six
import requests


class SlackRequest(object):

    @staticmethod
    def do(token, request="?", post_data=None, domain="slack.com"):
          '''
        Perform a POST request to the Slack Web API
        Args:
            token (str): your authentication token
            request (str): the method to call from the Slack API. For example: 'channels.list'
            post_data (dict): key/value arguments to pass for the request. For example:
                {'channel': 'CABC12345'}
            domain (str): if for some reason you want to send your request to something other
                than slack.com
        '''
        if post_data is None:
            post_data = {}

        if "files" in post_data:
            temp = {element:post_data[element] for element in post_data if not "files" in element}
            return requests.post(
            'https://{0}/api/{1}'.format(domain, request),
            data=dict(temp, token=token), files=post_data["files"]
            )
        else:
            return requests.post(
                'https://{0}/api/{1}'.format(domain, request),
                data=dict(post_data, token=token),
            )
