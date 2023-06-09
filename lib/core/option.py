import copy
import logging
import os
import re
import socket
from queue import Queue
from urllib.parse import urlsplit

import socks
from lib.core.clear import remove_extra_log_message
from lib.core.common import boldify_message, get_public_type_members
from lib.core.data import conf, cmd_line_options
from lib.core.data import kb
from lib.core.data import logger
from lib.core.data import merged_options
from lib.core.data import paths
from lib.core.datatype import AttribDict
from lib.core.enums import HTTP_HEADER, CUSTOM_LOGGING, PROXY_TYPE
from lib.core.exception import GeccoSyntaxException
from lib.core.log import FORMATTER
from lib.core.defaults import defaults
from lib.parse.configfile import config_file_parser


def set_verbosity():
    """
    This function set the verbosity of gecco output messages.
    """

    if conf.verbose is None:
        conf.verbose = 1

    conf.verbose = int(conf.verbose)

    if conf.verbose == 0:
        logger.setLevel(logging.ERROR)
    elif conf.verbose == 1:
        logger.setLevel(logging.INFO)
    elif conf.verbose == 2:
        logger.setLevel(logging.DEBUG)
    elif conf.verbose == 3:
        logger.setLevel(logging.DEBUG)
        logger.setLevel(CUSTOM_LOGGING.SYSINFO)
    elif conf.verbose == 4:
        logger.setLevel(logging.DEBUG)
        logger.setLevel(CUSTOM_LOGGING.WARNING)
    elif conf.verbose >= 5:
        logger.setLevel(logging.DEBUG)
        logger.setLevel(CUSTOM_LOGGING.ERROR)



def _set_http_cookie():
    if conf.cookie:
        if isinstance(conf.cookie, dict):
            conf.http_headers[HTTP_HEADER.COOKIE] = '; '.join(map(lambda x: '='.join(x), conf.cookie.items()))
        else:
            conf.http_headers[HTTP_HEADER.COOKIE] = conf.cookie




def _set_network_timeout():
    if conf.timeout:
        conf.timeout = float(conf.timeout)
        if conf.timeout < 3.0:
            warn_msg = "the minimum HTTP timeout is 3 seconds, gecco "
            warn_msg += "will going to reset it"
            logger.warn(warn_msg)

            conf.timeout = 3.0
    else:
        conf.timeout = 30.0

    socket.setdefaulttimeout(conf.timeout)


def _set_network_proxy():
    if conf.proxy:
        debug_msg = "setting the HTTP/SOCKS proxy for all network requests"
        logger.debug(debug_msg)

        try:
            _ = urlsplit(conf.proxy)
        except Exception as ex:
            err_msg = "invalid proxy address '{0}' ('{1}')".format(conf.proxy, str(ex))
            raise GeccoSyntaxException(err_msg)

        hostname_port = _.netloc.split(":")
        scheme = _.scheme.upper()
        hostname = hostname_port[0]
        port = None
        username = None
        password = None

        if len(hostname_port) == 2:
            try:
                port = int(hostname_port[1])
            except Exception:
                pass

        if not all((scheme, hasattr(PROXY_TYPE, scheme), hostname, port)):
            err_msg = "proxy value must be in format '({0})://address:port'".format("|".join(
                _[0].lower() for _ in get_public_type_members(PROXY_TYPE)))
            raise GeccoSyntaxException(err_msg)

        if conf.proxy_cred:
            _ = re.search(r"\A(.*?):(.*?)\Z", conf.proxy_cred)
            if not _:
                err_msg = "proxy authentication credentials "
                err_msg += "value must be in format username:password"
                raise GeccoSyntaxException(err_msg)
            else:
                username = _.group(1)
                password = _.group(2)
                
       
        if scheme in (PROXY_TYPE.SOCKS4, PROXY_TYPE.SOCKS5, PROXY_TYPE.SOCKS5H):
            
            socks.set_default_proxy(
                socks.PROXY_TYPE_SOCKS4 if scheme == PROXY_TYPE.SOCKS4 else socks.PROXY_TYPE_SOCKS5,
                hostname,
                port,
                username=username,
                password=password,
                rdns=True if scheme == PROXY_TYPE.SOCKS5H else False,
            )
            conf.origin_socks = copy.deepcopy(socket.socket)  # Convenient behind recovery
            socket.socket = socks.socksocket

        if conf.proxy_cred:
            proxy_string = "{0}@".format(conf.proxy_cred)
        else:
            proxy_string = ""

        proxy_string = "{scheme}://{proxy_string}{hostname}:{port}".format(scheme=scheme.lower(),
                                                                           proxy_string=proxy_string,
                                                                           hostname=hostname, port=port)
        conf.proxies = {
            "http": proxy_string,
            "https": proxy_string
        }
    else:
        conf.proxies = {}



def _set_threads():
    if not isinstance(conf.threads, int) or conf.threads <= 0:
        conf.threads = 1



def _adjust_logging_formatter():
    """
    Solves problem of line deletition caused by overlapping logging messages
    and retrieved data info in inference mode
    """
    if hasattr(FORMATTER, '_format'):
        return

    def new_format(record):
        message = FORMATTER._format(record)
        message = boldify_message(message)
        return message

    FORMATTER._format = FORMATTER.format
    FORMATTER.format = new_format


def _create_directory():
    if not os.path.isdir(paths.GECCO_OUTPUT_PATH):
        try:
            os.makedirs(paths.GECCO_OUTPUT_PATH)
            os.makedirs(paths.GECCO_TEMP_PATH)
        except FileExistsError:
            pass



def _set_conf_attributes():
    """
    This function set some needed attributes into the configuration
    singleton.
    """

    debug_msg = "initializing the configuration"
    logger.debug(debug_msg)

    conf.url = None
    for def_key, def_val in defaults.items():
        conf[def_key] = def_val



def _set_kb_attributes(flush_all=True):
    """
    This function set some needed attributes into the knowledge base
    singleton.
    """

    debug_msg = "initializing the knowledge base"
    logger.debug(debug_msg)
   
    kb.thread_continue = True
    kb.thread_exception = False
    kb.domain_list = []
    kb.sub_domain_list = []
    kb.task_queue = Queue()
    # kb.data = AttribDict()
    # kb.results = []
    



def _merge_options(input_options, override_options):
    """
    Merge command line options with configuration file and default options.
    """
    if hasattr(input_options, "items"):
        input_options_items = input_options.items()
    else:
        input_options_items = input_options.__dict__.items()
    for key, value in input_options_items:
        if key not in conf or value not in (None, False) or override_options:
            conf[key] = value

    if input_options.get("configFile"):
        config_file_parser(input_options["configFile"])

    merged_options.update(conf)




def init_options(input_options=AttribDict(), override_options=False):
    
    cmd_line_options.update(input_options)
    _set_conf_attributes()
   
    _set_kb_attributes()
    _merge_options(input_options, override_options)
    
    
    # if check version
    if conf.show_version:
        exit()

def init_network_conf():
    if any((conf.domain)):
        _set_http_cookie()

    _set_network_proxy()
    _set_network_timeout()



def init():
    """
    根据命令行和配置文件选项将属性设置到配置和知识库单例中
    """
    set_verbosity()
    _adjust_logging_formatter()
    _create_directory()

    _set_threads()
    remove_extra_log_message()
