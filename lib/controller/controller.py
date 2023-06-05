import copy
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import logger
from lib.core.exception import GeccoValidationException, GeccoSystemException
from lib.core.threads import run_threads


def runtime_check():
    # if not kb.registered_pocs:
    #     error_msg = "no PoC loaded, please check your PoC file"
    #     logger.error(error_msg)
    #     raise GeccoSystemException(error_msg)
    pass


def start():
    runtime_check()
    tasks_count = kb.task_queue.qsize()
    info_msg = "Gecco got a total of {0} tasks".format(tasks_count)
    logger.info(info_msg)
    logger.debug("Gecco will open {} threads".format(conf.threads))

    try:
        run_threads(conf.threads, task_run)
        logger.info("Scan completed,ready to print")
    finally:
        task_done()



def show_task_result():


    if not kb.results:
        return



def task_run():
    while not kb.task_queue.empty() and kb.thread_continue:
        target, poc_module, options, headers = kb.task_queue.get()
        if not conf.console_mode:
            poc_module = copy.deepcopy(kb.registered_pocs[poc_module])
        poc_name = poc_module.name

        try:
            pass
        except GeccoValidationException as ex:
            info_msg = "Poc:'{}' GeccoValidationException:{}".format(poc_name, ex)
            logger.error(info_msg)
            result = None


        






def task_done():
    show_task_result()
