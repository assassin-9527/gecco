import copy
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import logger
from lib.core.exception import GeccoValidationException, GeccoSystemException
from lib.core.threads import run_threads
from lib.core.common import get_domain, is_domain_format, is_url_format
from lib.modules.domain_collection import icp_search, whois_search


def runtime_check():

    if is_url_format(conf.domain):
        domain = get_domain(conf.domain)
    elif is_domain_format(conf.domain):
        domain = conf.domain
    else:
        domain = None

    if not domain:
        error_msg = "Please enter a valid domain name"
        logger.error(error_msg)
        raise GeccoSystemException(error_msg)
    else:
        kb.domain = domain
    



def start():
    runtime_check()
    info_msg = "Gecco got a domain {0}".format(kb.domain)
    logger.info(info_msg)
    logger.debug("Gecco will open {} threads".format(conf.threads))
    company_name = icp_search(kb.domain)
    company_name = whois_search(kb.domain)
    logger.info(company_name)



    # try:
    #     run_threads(conf.threads, task_run)
    #     logger.info("Scan completed,ready to print")
    # finally:
    #     task_done()



def show_task_result():


    if not kb.results:
        return



def task_run():
    while not kb.task_queue.empty() and kb.thread_continue:
       

        try:
            pass
        except GeccoValidationException as ex:
            info_msg = "GeccoValidationException"
            logger.error(info_msg)
            result = None


        






def task_done():
    show_task_result()
