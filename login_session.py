# This code used to be part of something bigger, but the main thing I wanted to save was the 
# login function. 

import requests
import os
from urllib.parse import urlencode


class Downloader:
    website = os.environ['TEST_WEB_SITE']
    session = requests.Session()

    def login_user(self):
        """Logs the user in, storing the necessary cookies in our session.

        :return: True if logged in, false otherwise.
        """
        login_url = 'ADD LOGIN URL'
        post_url = '{website}{login_url}'.format(website=self.website, login_url=login_url)
        headers = {
            'ADD': 'HEADERS HERE',
        }
        login_params = {
            'username': os.environ['TEST_WEB_USER'],
            'password': os.environ['TEST_WEB_PSWD'],
        # May need to add more login parameters, based on specific use cases
        }

        req = requests.Request('POST', post_url, headers=headers).prepare()
        req.body = urlencode(login_params)
        req.headers['Content-Length'] = len(req.body)
        self.session.send(req)

        # The use case I wrote this for only set cookies if it logged in -- that may not always
        # be true, so you may need to modify this check. 
        if len(self.session.cookies) == 0:
            return False
        else:
            return True

