from lib.request import requests
from lib.core.data import logger
from lib.core.data import kb
from lib.core.enums import CUSTOM_LOGGING
import re

#  域名收集模块 (Domain name collection)

class DomainCollection():

    def __init__(self, domain) -> None:
        self.domain = domain

    def icp_search(self):
        req_url = f"https://icp.aizhan.com/{self.domain}/"
        headers = {
            "Referer": "https://icp.aizhan.com/"
        }
        respon = requests.get(req_url, headers=headers, verify=False, allow_redirects=False)
        if respon:
            registrant_ret = re.search(r"主办单位名称</td>\s*<td>(.*?)&nbsp;", respon.text)
            if registrant_ret:
                return registrant_ret.group(1).strip()


    def whois_search(self):
        req_url = f"https://whois.aizhan.com/{self.domain}/"
        headers = {
            "Referer": "https://whois.aizhan.com/"
        }
        respon = requests.get(req_url, headers=headers, verify=False, allow_redirects=False)
        if respon:
            registrant_ret = re.search(r"域名持有人/机构名称</td>\s*<td>(.*?)<a", respon.text)
            if registrant_ret:
                return registrant_ret.group(1).strip()

    def registrant_reverse(self, registrant):
        req_url = f"https://whois.aizhan.com/reverse-whois?t=registrant&q={registrant}"
        headers = {
            "Referer": "https://whois.aizhan.com"
        }
        respon = requests.get(req_url, headers=headers, verify=False, allow_redirects=False)
        if respon:
            html_list = re.findall(r'<td class="url domain">(?:(?:.|\r|\n)*?)</td>', respon.text)
            for td_label in html_list:
                sh_domain = re.search(r'<a.*?>(.*?)</a>', td_label)
                if sh_domain:
                    kb.domain_list.append(sh_domain.group(1))

    def search(self):
        registrant = self.icp_search() or self.whois_search()
        if registrant:
            logger.info(f"注册人：{registrant}")
            kb.registrant = registrant
            self.registrant_reverse(registrant=registrant)
        
        if kb.domain not in kb.domain_list:
            kb.domain_list.append(kb.domain)
        logger.log(CUSTOM_LOGGING.SUCCESS, "搜索到域名列表(%s个)：%s" % (len(kb.domain_list), kb.domain_list))
        

    

