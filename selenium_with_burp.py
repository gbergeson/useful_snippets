from selenium import webdriver
import time


def main():
    """This script simply requests many urls with a selenium driver. It is intended to be used with BurpSuite Community
    Edition, which throttles the speed of attacks. BurpSuite will record the requests and responses, so no further
    processing is required once the url has been requested.

    In the initial round of testing, I immediately realized that selenium is much too slow for this purpose. Refactoring
    code to use requests instead, but saving this code for later.
    """

    target_url = input('Please input the base URL to attack (format: http://google.com): ')
    wordlist_file = input('Please input the wordlist of directories to check for (default is '
                          '/usr/share/dirbuster/wordlists/directory-list-2.3-small.txt for Kali): ')
    if wordlist_file == '':
        wordlist_file = '/usr/share/dirbuster/wordlists/directory-list-2.3-small.txt'

    with open(wordlist_file) as f:
        full_text = f.read()

    # These two lines are for testing speed
    dirs = full_text.split('\n')
    dirs = dirs[:100]

    t0 = time.perf_counter()
    driver = firefox_driver_proxy()

    for test_dir in dirs:
        url = '{}{}'.format(target_url, test_dir)
        driver.get(url)
    t1 = time.perf_counter()
    time_elapsed = t1 - t0

    print("Completed {} requests in {} seconds.".format(len(dirs), time_elapsed))


def firefox_driver_proxy(proxy='127.0.0.1:8080'):
    """Configure a selenium webdriver for Firefox with a proxy server.
    Adapted from the first answer to the question at
    https://stackoverflow.com/questions/51893564/firefox-with-selenium-and-python-proxy-issues
    
    :param proxy: The proxy address to connect to (default 127.0.0.1:8080)
    :return: The driver with the proxy configured
    """
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['proxy'] = {"proxyType": "MANUAL", "httpProxy": proxy, "ftpProxy": proxy, "sslProxy": proxy}

    fp = webdriver.FirefoxProfile()
    fp.update_preferences()

    proxy_driver = webdriver.Firefox(capabilities=firefox_capabilities, firefox_profile=fp)

    return proxy_driver


if __name__ == '__main__':
    main()
