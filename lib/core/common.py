# pylint: disable=E1101
import inspect
import os
import re
import sys
import collections
from colorama.initialise import init as coloramainit
from lib.core.decorators import cachedmethod
from termcolor import colored
from lib.core.convert import stdout_encode
from lib.core.data import paths
from lib.core.exception import GeccoSystemException
from lib.core.log import LOGGER_HANDLER
from lib.core.settings import BANNER, BOLD_PATTERNS, IS_WIN, URL_DOMAIN_REGEX
from lib.core.settings import IP_ADDRESS_REGEX
from lib.core.settings import UNICODE_ENCODING
from lib.core.settings import URL_ADDRESS_REGEX
from urllib.parse import urlparse

try:
    collectionsAbc = collections.abc
except AttributeError:
    collectionsAbc = collections


def read_binary(filename):
    content = ''
    with open(filename, 'rb') as f:
        content = f.read()
    return content


def check_path(path):
    return True if path and os.path.exists(path) else False


def check_file(filename):
    """
    @function Checks for file existence and readability
    """

    valid = True

    if filename is None or not os.path.isfile(filename):
        valid = False

    if valid:
        try:
            with open(filename, "rb"):
                pass
        except Exception:
            valid = False

    if not valid:
        raise GeccoSystemException("unable to read file '%s'" % filename)
    return valid


def set_paths(root_path):
    """
    Sets absolute paths for project directories and files
    """
    paths.GECCO_ROOT_PATH = root_path
    paths.GECCO_DATA_PATH = os.path.join(paths.GECCO_ROOT_PATH, "data")
    paths.GECCO_TEMP_PATH = os.path.join(paths.GECCO_ROOT_PATH, "temp")

    paths.GECCO_OUTPUT_PATH = paths.get("GECCO_OUTPUT_PATH", os.path.join(paths.GECCO_ROOT_PATH, "output"))


def banner():
    """
    Function prints gecco banner with its version
    """
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = clear_colors(_)
    elif IS_WIN:
        coloramainit()

    data_to_stdout(_)


def set_color(message, bold=False):
    if isinstance(message, bytes):
        message = message.decode(UNICODE_ENCODING)
    ret = message

    if message and getattr(LOGGER_HANDLER, "is_tty", False):  # colorizing handler
        if bold:
            ret = colored(message, color=None, on_color=None, attrs=("bold",))

    return ret


def clear_colors(message):
    ret = message
    if message:
        ret = re.sub(r"\x1b\[[\d;]+m", "", message)
    return ret


@cachedmethod
def get_public_type_members(type_, only_values=False):
    """
    Useful for getting members from types (e.g. in enums)
    """
    ret = []
    for name, value in inspect.getmembers(type_):
        if not name.startswith("__"):
            if not only_values:
                ret.append((name, value))
            else:
                ret.append(value)
    return ret


def boldify_message(message):
    ret = message

    if any(_ in message for _ in BOLD_PATTERNS):
        ret = set_color(message, bold=True)

    return ret


def data_to_stdout(data, bold=False):
    """
    Writes text to the stdout (console) stream
    """
    message = ""

    if isinstance(data, str):
        message = stdout_encode(data)
    else:
        message = data
    sys.stdout.write(set_color(message, bold))
    try:
        sys.stdout.flush()
    except IOError:
        pass




def is_url_format(value):
    if value and re.match(URL_ADDRESS_REGEX, value):
        return True
    else:
        return False


def is_domain_format(value):
    if value and re.match(URL_DOMAIN_REGEX, value):
        return True
    else:
        return False



def get_domain(url):
    """
    获取url的domain
    """
    urlinfo = urlparse(url)
    domain = urlinfo.netloc.split(':')[0]
    if not re.search(IP_ADDRESS_REGEX, domain):
        if urlinfo.netloc.find('.') != -1:
            domain_spt = urlinfo.netloc.split('.')
            domain = "%s.%s" % (domain_spt[-2], domain_spt[-1])
    return domain


def read_file2arr(file_path):
    """
    读取文件并以'\n'换行符拆分为数组返回
    """
    with open(file=file_path, mode="r", encoding="utf-8") as fd:
        return fd.readlines()


def unique_strlist(str_list:list):
    """
    字符列表去重去空
    """
    tmp_list = []
    for str_val in str_list:
        str = str_val.strip()
        if str:
            tmp_list.append(str)
    return set(tmp_list)
