from lib.request import requests
from lib.core.data import logger
import re

#  域名收集模块 (Domain name collection)

class DomainCollection():

    def __init__(self, domain) -> None:
        self.domain = domain

    def icp_search(domain):
        req_url = f"https://icp.aizhan.com/{domain}/"
        headers = {
            "Referer": "https://icp.aizhan.com/"
        }
        respon = requests.get(req_url, headers=headers, verify=False, allow_redirects=False)
        if respon:
            registrant_ret = re.search(r"主办单位名称</td>\s*<td>(.*?)&nbsp;", respon.text)
            if registrant_ret:
                return registrant_ret.group(1).strip()


    def whois_search(domain):
        req_url = f"https://whois.aizhan.com/{domain}/"
        headers = {
            "Referer": "https://whois.aizhan.com/"
        }
        respon = requests.get(req_url, headers=headers, verify=False, allow_redirects=False)
        if respon:
            registrant_ret = re.search(r"域名持有人/机构名称</td>\s*<td>(.*?)<a", respon.text)
            if registrant_ret:
                return registrant_ret.group(1).strip()

    def registrant_reverse(self):
        pass

    def search(self):
        registrant = None
        pass

    

