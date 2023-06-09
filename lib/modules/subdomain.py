import itertools as it
from dns import resolver, rdatatype
from lib.core.data import logger
from lib.core.common import read_file2arr, unique_strlist
from lib.core.work_helper import WorkHelper
from lib.core.data import kb
from lib.core.enums import CUSTOM_LOGGING
from lib.core.data import paths
from lib.core.data import conf
from lib.core.threads import run_threads
from lib.core.exception import GeccoValidationException

#  子域名爆破模块 ( Subdomain blasting module )

class DNSResult():
    def __init__(self, item) -> None:
        if item.rdtype == rdatatype.A:
            self.text = item.to_text()
        elif item.rdtype == rdatatype.CNAME:
            self.text = item.to_text().rstrip(".")
        self.rdtype = item.rdtype
        self.next = None
    
    def set_next(self, item):
        self.next = DNSResult(item)



class SubDomain():
    def __init__(self, domain_list) -> None:
        self.sub_list = []
        self.domain_list = domain_list
        self.resolvers_file_path = "data/resolvers.txt"
        self.sub_file_path = "data/sub_domain.txt"
        kb.resolvers_list = self.get_resolver_list()
        if not kb.resolvers_list: return
        # self.auto_generate_subdomain(len=1)
        # self.auto_generate_subdomain(len=2)
        # self.auto_generate_subdomain(len=3)
        self.dict_generate_subdomain()
        self.max_retry_count = 3          # 超时重试最大3次
        self.timeout_subdomain_list = []  # 记录超时子域名
    
    def get_resolver_list(self):
        resolvers_list = unique_strlist(read_file2arr(self.resolvers_file_path))
        def __filter_valid_worker(name_server):
            try:
                dns_client = resolver.Resolver()
                dns_client.nameservers = [name_server]
                dns_client.lifetime = 1
                answers = dns_client.query(qname="public1.114dns.com", rdtype = rdatatype.A)
                for rdata in answers:
                    if "114.114.114.114" == rdata.address:
                        return name_server
            except:
                pass
        work_th = WorkHelper(resolvers_list, len(resolvers_list))
        work_th.work = __filter_valid_worker
        work_th.run()
        return work_th.result_list


    def append_brute_success(self, sub_domain):
        if sub_domain not in kb.sub_domain_list:
            kb.sub_domain_list.append(sub_domain) 
            logger.log(CUSTOM_LOGGING.SUCCESS, "SUCCESS : %s" % sub_domain)

    def auto_generate_subdomain(self, len=1):
        dd = "abcdefghijklmzopqrstuvwxyz0123456789"
        for e in it.product(dd, repeat=len):
            sub_str = "".join(e)
            self.sub_list.append(sub_str)
            for domain in self.domain_list:
                sub_domain = "%s.%s" % (sub_str, domain)
                kb.task_queue.put(sub_domain)

    def dict_generate_subdomain(self):
        with open(self.sub_file_path, mode="r") as fd:
            lines = set(fd.readlines())
        for line in lines:
            sub_str = line.strip()
            for domain in self.domain_list:
                sub_domain = "%s.%s" % (sub_str, domain)
                kb.task_queue.put(sub_domain)

    def brute_sub_domain(self, sub_domain):
        try:
            logger.info(f"DNS => {sub_domain}")
            dns_client = resolver.Resolver()
            dns_client.nameservers = kb.resolvers_list
            dns_client.lifetime = 2
            answers = dns_client.query(qname=sub_domain, rdtype = rdatatype.A)
            if answers:
                self.append_brute_success(sub_domain)
        except resolver.NXDOMAIN:
            pass
        except resolver.Timeout:
            if sub_domain not in self.timeout_subdomain_list:
                self.timeout_subdomain_list.append(sub_domain)
        except BaseException:
            pass
    
    def timeout_retry(self):
        # 超时重试最大3次
        max_retry_count = 3
        for i in range(max_retry_count):
            if not self.timeout_subdomain_list: break
            index = len(self.timeout_subdomain_list) - 1
            while index >= 0:
                sub_domain = self.timeout_subdomain_list[index]
                logger.info(f"DNS => {sub_domain}")
                try:
                    logger.info(f"DNS => {sub_domain}")
                    dns_client = resolver.Resolver()
                    dns_client.nameservers = kb.resolvers_list
                    dns_client.lifetime = 2
                    answers = dns_client.query(qname=sub_domain, rdtype = rdatatype.A)
                    if answers:
                        del self.timeout_subdomain_list[index]
                        self.append_brute_success(sub_domain)
                except resolver.NXDOMAIN:
                    pass
                except resolver.Timeout:
                    pass
                except BaseException:
                    pass
                index -= 1

    
    def start_brute(self):
        def task_run():
            while not kb.task_queue.empty() and kb.thread_continue:
                try:
                    sub_domain = kb.task_queue.get()
                    self.brute_sub_domain(sub_domain)
                except GeccoValidationException as ex:
                    logger.error(ex)
        run_threads(conf.threads, task_run)
        self.timeout_retry()
        logger.log(CUSTOM_LOGGING.SUCCESS, "爆破到子域名列表(%s个)：%s" % (len(kb.sub_domain_list), kb.sub_domain_list))
