import copy
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import logger
from lib.core.exception import GeccoValidationException, GeccoSystemException, GeccoBaseException
from lib.core.threads import run_threads
from lib.core.common import get_domain, is_domain_format, is_url_format
from lib.modules.domain_collection import DomainCollection
from lib.modules.subdomain import SubDomain


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
    try:
        runtime_check()
        logger.info("输入域名 => {0}".format(kb.domain))
        logger.debug("最大允许使用的线程数: {} ".format(conf.threads))
        domain_search_step()
        subdomain_step()
    except GeccoBaseException as ex:
        logger.error(ex)

def domain_search_step():
    # 域名收集阶段
    try:
        dc = DomainCollection(kb.domain)
        dc.search()
    finally:
        pass

def subdomain_step():
    # 子域名爆破阶段
    try:
        logger.info("开始进行子域名爆破...")
        sbd = SubDomain(domain_list=kb.domain_list)
        sbd.start_brute()
        
    finally:
        pass



