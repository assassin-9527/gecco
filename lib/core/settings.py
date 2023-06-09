import sys
import time
import os
from platform import system, machine

from lib.core.revision import get_revision_number

VERSION = '1.0.0'
REVISION = get_revision_number()
TAG = "wyc"
VERSION_STRING = "Gecco/%s%s" % (
    VERSION,
    "-%s" % REVISION
    if REVISION
    else "-nongit-%s"
    % time.strftime(
        "%Y%m%d",
        time.gmtime(
            os.path.getctime(
                __file__.replace(".pyc", ".py")
                if __file__.endswith("pyc")
                else __file__
            )
        ),
    ),
)

IS_WIN = True if (sys.platform in ["win32", "cygwin"] or os.name == "nt") else False
PLATFORM = os.name
PYVERSION = sys.version.split()[0]


LEGAL_DISCLAIMER = (
    "Usage of pocsuite for attacking targets without prior mutual consent is illegal."
)


BANNER = """\033[01;33m
  _______              _             \033[01;37m{\033[01;%dm%s\033[01;37m}\033[01;33m
 |__   __|            | |          
    | | ___ _ __   ___| |__  _   _ 
    | |/ _ \ '_ \ / __| '_ \| | | |
    | |  __/ | | | (__| | | | |_| |
    |_|\___|_| |_|\___|_| |_|\__,_|  \033[0m\033[4;37m%s\033[0m     

""" % (
    (31 + hash(REVISION) % 6) if REVISION else 30,
    VERSION_STRING.split("/")[-1],
    TAG,
)

BANNER = """\033[01;33m
  ▄████ ▓█████  ▄████▄   ▄████▄   ▒█████     \033[01;37m{\033[01;%dm%s\033[01;37m}\033[01;33m
 ██▒ ▀█▒▓█   ▀ ▒██▀ ▀█  ▒██▀ ▀█  ▒██▒  ██▒
▒██░▄▄▄░▒███   ▒▓█    ▄ ▒▓█    ▄ ▒██░  ██▒
░▓█  ██▓▒▓█  ▄ ▒▓▓▄ ▄██▒▒▓▓▄ ▄██▒▒██   ██░
░▒▓███▀▒░▒████▒▒ ▓███▀ ░▒ ▓███▀ ░░ ████▓▒░
 ░▒   ▒ ░░ ▒░ ░░ ░▒ ▒  ░░ ░▒ ▒  ░░ ▒░▒░▒░ 
  ░   ░  ░ ░  ░  ░  ▒     ░  ▒     ░ ▒ ▒░ 
░ ░   ░    ░   ░        ░        ░ ░ ░ ▒  
      ░    ░  ░░ ░      ░ ░          ░ ░     
               ░        ░                    \033[0m\033[4;37m%s\033[0m  
""" % (
    (31 + hash(REVISION) % 6) if REVISION else 30,
    VERSION_STRING.split("/")[-1],
    TAG,
)

# Encoding used for Unicode data
UNICODE_ENCODING = "utf-8"


# Regular expression used for recognition of IP addresses
IP_ADDRESS_REGEX = r"\b(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\b"
URL_ADDRESS_REGEX = r"(?:(?:https?):\/\/|www\.|ftp\.)(?:\([-a-zA-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-a-zA-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-a-zA-Z0-9+&@#\/%=~_|$?!:,.]*\)|[a-zA-Z0-9+&@#\/%=~_|$])"
URL_DOMAIN_REGEX = (
    r"(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,3})(?:/[\w&%?#-]{1,300})?(?:\:\d+)?"
)


POC_REQUIRES_REGEX = r"install_requires\s*=\s*\[(?P<result>.*?)\]"

POC_NAME_REGEX = r"""(?sm)POCBase\):.*?name\s*=\s*['"](?P<result>.*?)['"]"""

MAX_NUMBER_OF_THREADS = 20

DEFAULT_LISTENER_PORT = 6666

# Maximum number of lines to save in history file
MAX_HISTORY_LENGTH = 1000

IMG_EXT = (".jpg", ".png", ".gif")


BOLD_PATTERNS = (
    "' is vulnerable",
    "success",
    "\d    ",
)

