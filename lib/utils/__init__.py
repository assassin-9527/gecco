import re
import ast
import string
import random
from faker import Faker
from socket import gethostbyname
import urllib.parse
from lib.core.data import logger
from lib.core.enums import (
    CUSTOM_LOGGING
)


def urlparse(address):
    if not re.search(r'^[A-Za-z0-9+.\-]+://', address):
        address = 'tcp://{0}'.format(address)
    return urllib.parse.urlparse(address)


def url2ip(url, with_port=False):
    """
    works like turning 'http://baidu.com' => '180.149.132.47'
    """

    url_prased = urlparse(url)
    if url_prased.port:
        ret = gethostbyname(url_prased.hostname), url_prased.port
    elif not url_prased.port and url_prased.scheme == 'https':
        ret = gethostbyname(url_prased.hostname), 443
    else:
        ret = gethostbyname(url_prased.hostname), 80

    return ret if with_port else ret[0]


def str_to_dict(value):
    try:
        return ast.literal_eval(value)
    except ValueError as e:
        logger.log(CUSTOM_LOGGING.ERROR, "conv string failed : {}".format(str(e)))


def random_str(length=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.sample(chars, length))


def generate_random_user_agent():
    return Faker().user_agent()

