__author__ = 'mysteq'
import logging
import requests
import urllib2, urllib
import sys
import json
import pprint
logging.basicConfig(level=logging.DEBUG)
TOKEN_FILENAME = ".secret"
INBOX_URL = "/me/inbox"
GRAPH_HOST = "https://graph.facebook.com"

"""
TODO: Czytanie threadow
TODO: Zadawanie threadow do zrzucania plus predkosc
"""


class MyThreadMessage(object):
    def __init__(self, message_data):
        self.id = message_data['id']
        self.from_user = message_data['from']
        self.message = message_data['message']
        self.created_time = message_data['created_time']

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"[{0}] {1}: {2}".format(self.created_time, self.from_user['name'], self.message)


class MyThreadComment(object):
    def __init__(self, thread_comment_data):
        self.data = thread_comment_data['data']
        self.paging = thread_comment_data['paging']
        self.messages = [MyThreadMessage(x) for x in self.data]


class MyThread(object):
    def __init__(self, thread_data):
        self.id = thread_data['id']
        self.to = thread_data['to']
        self.unread = thread_data['unread']
        self.unseen = thread_data['unseen']
        self.updated_time = thread_data['updated_time']
        self.comment = MyThreadComment(thread_data['comments'])

    def unseen(self):
        return self.unseen

    def unread(self):
        return self.unread

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def get_messages(self):
        return self.comment.messages


def read_access_token():
    """
    :return: zwraca token z pliku TOKEN_FILENAME
    """
    logger = logging.getLogger(__name__)
    token = None
    with open(TOKEN_FILENAME, 'r') as token_file:
        logger.debug("reading access token from {0}".format(TOKEN_FILENAME))
        token = token_file.readline()
    return token


def read_inbox(inbox_url=INBOX_URL):
    """
    Funkcja zaczytuje skrzynke odbiorcza i wywala na ekran konwersacje
    :param inbox_url: url do skrzynki z wiadomosciami (z reguly /me/inbox )
    :return: odpowiedz ze skrzynki odbiorczej w formacie JSON
    """
    logger = logging.getLogger(__name__)
    url_inbox = GRAPH_HOST+INBOX_URL
    req_params = dict()
    req_params['access_token'] = read_access_token()
    r = requests.get(url_inbox, params=req_params)
    logger.debug("response encoding: {0}".format(r.encoding))
    return r.json()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    print read_access_token()
    inbox_json_response = read_inbox()
    try:
        inbox_data = inbox_json_response['data']
        inbox_paging = inbox_json_response['paging']
        inbox_summary = inbox_json_response['summary']
        my_thread = MyThread(inbox_data[0])
        print [x.__str__() for x in my_thread.get_messages()]
    except KeyError:
        logger.error("Key Error.")
        logger.error(inbox_json_response['error'])

    #logger.debug(inbox_data)
    #parsed_thread_data = json.loads(inbox_data, encoding='unicode')

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(inbox_data)

