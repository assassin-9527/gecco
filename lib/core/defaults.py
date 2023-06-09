from lib.core.datatype import AttribDict

_defaults = {
    "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "headers": None,
    "proxy": None,
    "proxy_cred": None,
    "proxies": {},
    "timeout": 30,
    "threads": 20,
    "verbose": 1,
    "show_version": False,
    "domain": "",
    "cookie": None,

}

defaults = AttribDict(_defaults)

