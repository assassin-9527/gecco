import os
import sys
import threading
import time
import traceback


from lib.core.option import init
from lib.core.option import init_options, init_network_conf
from lib.core.exception import GeccoUserQuitException, GeccoSystemException
from lib.core.exception import GeccoShellQuitException
from lib.core.common import set_paths
from lib.core.common import banner
from lib.core.common import data_to_stdout
from lib.core.data import logger
from lib.parse.cmd import cmd_line_parser
from lib.controller.controller import start
from lib.core.data import conf
from lib.request.patch import patch_all



def module_path():
    """
    获取程序的目录
    """
    return os.path.dirname(os.path.realpath(__file__))


def check_environment():
    try:
        os.path.isdir(module_path())
    except Exception:
        err_msg = "您的系统无法正确处理中文路径， "
        err_msg += "请移动到其它目录"
        logger.critical(err_msg)
        raise SystemExit



import datetime
def main():
    try:
        starttime = datetime.datetime.now()
        check_environment()
        set_paths(module_path())
        banner()
        init_options(cmd_line_parser().__dict__)
        patch_all()
        data_to_stdout("[*] starting at {0}\n\n".format(time.strftime("%X")))
        init_network_conf()
        init()
        try:
            start()
        except threading.ThreadError:
            raise
        
    except GeccoUserQuitException:
        pass

    except GeccoShellQuitException:
        pass

    except GeccoSystemException:
        pass

    except KeyboardInterrupt:
        pass

    except EOFError:
        pass

    except SystemExit:
        pass

    except Exception:
        exc_msg = traceback.format_exc()
        data_to_stdout(exc_msg)
        raise SystemExit

    finally:
        endtime = datetime.datetime.now()
        runtime = (endtime - starttime).seconds
        data_to_stdout("\n[*] shutting down at {0}, runtime: {1}\n\n".format(time.strftime("%X"), runtime))


if __name__ == "__main__":
    main()
