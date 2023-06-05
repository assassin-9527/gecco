import sys
import os
import logging
import colorlog
from logging.handlers import TimedRotatingFileHandler
from lib.core.enums import CUSTOM_LOGGING

logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")

LOGGER = logging.getLogger("gecco")
try:
    # for python>=3.7
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    # http://www.macfreek.nl/memory/Encoding_of_Python_stdout
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
PRIMARY_FMT = (
    "%(cyan)s[%(asctime)s] %(log_color)s[%(levelname)s]%(reset)s %(message)s"
)
CUSTOM_FMT = "%(log_color)s[%(asctime)s] [%(levelname)s] %(message)s"

FORMATTER = colorlog.LevelFormatter(
    fmt={
        "DEBUG": PRIMARY_FMT,
        "INFO": PRIMARY_FMT,
        "WARNING": PRIMARY_FMT,
        "ERROR": PRIMARY_FMT,
        "CRITICAL": PRIMARY_FMT,
        "*": CUSTOM_FMT,
        "+": CUSTOM_FMT,
        "-": CUSTOM_FMT,
        "!": CUSTOM_FMT
    },
    datefmt="%H:%M:%S",
    log_colors={
        '*': 'cyan',
        '+': 'green',
        '-': 'red',
        '!': 'yellow',
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bg_red,white'
    },
    secondary_log_colors={},
    style='%'
)

disableColor = "disable-col" in ' '.join(sys.argv)
if disableColor:
    FORMATTER = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")


LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(logging.INFO)

def __getFileNameByLevel__(level, filename):
    if level == logging.ERROR:
        return f"{filename}_error"
    elif level == logging.INFO:
        return f"{filename}_info"
    elif level == logging.DEBUG:
        return f"{filename}_debug"
    elif level == logging.WARNING:
        return f"{filename}_warning"

def setFileHandler(level=None, log_path='./logs', log_filename='gecco'):
    """
    set file handler
    :param level:
    :return:
    """
    filename = __getFileNameByLevel__(level, log_filename)
    file_name = os.path.join(log_path, '{name}.log'.format(name=filename))
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
    file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
    file_handler.suffix = '%Y%m%d.log'
    file_handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - [%(threadName)s] - (%(filename)s).%(funcName)s (%(lineno)d) - %(message)s")
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)

setFileHandler(logging.INFO)
