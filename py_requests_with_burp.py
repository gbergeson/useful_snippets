# Some useful requests snippets I didn't end up using the way I thought I would... but putting here to save for later.
# I could have used dirbuster with a custom wordlist, but wanted to do it this way, to record results in Burp and to
# learn some more about python requests.
# TODO: Fix the multithreading

from concurrent.futures.thread import ThreadPoolExecutor
import requests
import time


class Discover:
    target_url = ''
    base_directory = ''
    wordlist_file = ''

    def master_task(self):
        """This script simply requests many urls with the requests library. It is intended to circumvent how BurpSuite
        Community Edition throttles the speed of attacks--this can do it much faster. BurpSuite will record the requests
        and responses, so no further processing is required once the url has been requested.

        """

        self.target_url = input('Base URL to attack: ') or 'WHATEVER YOU WANT'
        self.base_directory = input('Base directory to bruteforce: ') or 'WHATEVER YOU WANT'

        default_filename = 'WHATEVER YOU WANT'
        self.wordlist_file = input('Please input the wordlist of directories to check for: ') or default_filename

        with open(self.wordlist_file) as f:
            full_text = f.read()
        test_strs = full_text.split('\n')

        '''
        # Testing two methods for speed: environment variables and mapping proxy
        # Env. vars result =
        # Mapping proxy result =
        proxies = {
            'http': '127.0.0.1:8080',
            'https': '127.0.0.1:8080'
        }
        '''

        test_ints = []
        for test_str in test_strs[:-1]:
            test_ints.append(int(test_str))

        urls_to_check = test_ints[1100:1200]
        num_worker_threads = 4

        t0 = time.perf_counter()

        with ThreadPoolExecutor(max_workers=num_worker_threads) as executor:
            results = executor.map(self.check_url, urls_to_check)

        t1 = time.perf_counter()
        time_elapsed = t1 - t0

        print("Completed {} requests in {} seconds.".format(len(urls_to_check), time_elapsed))
        print("Average time per request: {}".format(str(time_elapsed / len(urls_to_check))))
        print(results)

        return results

# This function was built with a very specific use case in mind, can ignore it/modify it.
    def check_url(self, urls_to_check):
        base_url = '{}{}'.format(self.target_url, self.base_directory)
        valid_urls = []

        for url in urls_to_check:
            url = '{}{}'.format(base_url, str(url))
            r = requests.get(url, allow_redirects=False)
            if 'REDIRECT LOCATION' not in r.headers['Location']:
                valid_urls.append(url)
                print(r.headers['Location'])

        return valid_urls
