# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


import random
import re
import threading
import socks
import socket
import time
import urllib.request



user_agents = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
]


# try:
#     with open("user_agents.txt", "r+") as f:
#         for line in f.readlines():
#             user_agents.append(line.replace("\n", ""))
# except FileNotFoundError:
#     pass


class Proxy:
    def __init__(self, method: str, proxy: str) -> None:
        if method.lower() not in ["http", "https", "socks4", "socks5"]:
            raise NotImplementedError("Only HTTP, HTTPS, SOCKS4, and SOCKS5 are supported")
        self.method = method
        self.proxy = proxy


    def isValid(self):
        return re.match(r"\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})?$", self.proxy)
    
    def check(self, site: str, timeout, user_agent: str):
        if self.method in ["socks4", "socks5"]:
            socks.set_default_proxy(socks.SOCKS4 if self.method == "socks4" else socks.SOCKS5,
                                    self.proxy.split(':')[0], int(self.proxy.split(':')[1]))
            socket.socket = socks.socksocket

            try:
                start_time = time.time()
                urllib.request.urlopen(site, timeout=timeout)
                end_time = time.time()
                time_taken = end_time - start_time
                print(f"[ {time_taken}s ] ( {self.proxy} ) Valid")
                return True, time_taken, None
            except Exception as e:
                print(e)
                return False, 0, e
            

        else:
            url = self.method + "://" + self.proxy
            proxy_support = urllib.request.ProxyHandler({self.method: url})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
            req = urllib.request.Request(self.method + "://" + site)
            req.add_header("User-Agent", user_agent)
            try:
                start_time = time.time()
                urllib.request.urlopen(req, timeout=timeout)
                end_time = time.time()
                time_taken = end_time - start_time
                print(f"[ {time_taken}s ] ( {self.proxy} ) Valid")
                return True, time_taken, None
            except Exception as e:
                print(e)
                return False, 0, e


    def __str__(self):
        return self.proxy


def check(file: str, timeout, method, site, random_user_agent):
    proxies = []
    with open(file, "r+") as f:
        for line in f:
            proxies.append(Proxy(method, line.replace("\n", "")))

    print(f"Checking {len(proxies)} proxies")
    proxies = filter(lambda x: x.isValid(), proxies)
    valid_proxies = []
    user_agent = random.choice(user_agents)

    def check_proxy(proxy: Proxy, user_agent: str):
        new_user_agent = user_agent
        if random_user_agent:
            new_user_agent = random.choice(user_agents)
        valid, time_taken, error = proxy.check(site, timeout, new_user_agent)
        valid_proxies.extend([proxy] if valid else [])

    threads = []
    for proxy in proxies:
        t = threading.Thread(target=check_proxy, args=(proxy, user_agent))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    with open("./input/proxies.txt", "w") as f:
        for proxy in valid_proxies:
            f.write(str(proxy) + "\n")

    print(f"Found {len(valid_proxies)} valid proxies")


def run_checker(filepath: str = './input/scraped_http.txt', timeout: int = 10, method: str = 'http', site: str = "https://google.com"):
    check(file=filepath, timeout=timeout, method=method, site=site,
          random_user_agent=random.choice(user_agents))


if __name__ == "__main__":
    run_checker()