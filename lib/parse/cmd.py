import argparse
import os
import sys

from lib.core.common import data_to_stdout
from lib.core.settings import IS_WIN

DIY_OPTIONS = []


def cmd_line_parser(argv=None):
    """
    This function parses the command line parameters and arguments
    """

    if not argv:
        argv = sys.argv

    _ = os.path.basename(argv[0])
    usage = "gecco [options]"
    parser = argparse.ArgumentParser(prog='Gecco', usage=usage)
    try:
        parser.add_argument("--version", dest="show_version", action="store_true",
                            help="Show program's version number and exit")

        parser.add_argument("--update", dest="update_all", action="store_true",
                            help="Update Gecco")
        
        parser.add_argument("-d", "--domain", dest="domain", required=True, help="Target domain (e.g. \"www.site.com\")")
        parser.add_argument("--proxy", dest="proxy", help="Use a proxy to connect to the target URL")
        parser.add_argument("--proxy-cred", dest="proxy_cred", help="Proxy authentication credentials (name:password)")
        parser.add_argument("--threads", dest="threads", type=int, default=1, help="Max number of concurrent network requests")
        
        args = parser.parse_args()
        
        return args

    except SystemExit:
        # Protection against Windows dummy double clicking
        if IS_WIN:
            data_to_stdout("\nPress Enter to continue...")
            input()
        raise
