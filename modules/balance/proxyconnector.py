# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------

import tls_client
import random

from .. import config

def loadProxies(proxyfile: str = config["proxyfile"]) -> list[str] | None:
    return [line.strip() for line in open(proxyfile, "r+").readlines()]



available_browser_spoof = [
    {
        'name': 'iPhone | iOS 18',
        'client_identifier': 'safari_ios_18_0',
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'
    },
    {
        'name': 'iPhone | iOS 17',
        'client_identifier': 'safari_ios_17_0',
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    },
    {
        'name': 'Chrome | Windows NT',
        'client_identifier': 'chrome_129',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    },
    {
        'name': 'Chrome | Linux',
        'client_identifier': 'chrome_134',
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    },
    {
        'name': 'Chrome | Windows NT',
        'client_identifier': 'chrome_128',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    },
    {
        'name': 'Chrome | Linux',
        'client_identifier': 'chrome_133',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
]



class StealthConnection:
    def __init__(self, use_proxy: bool = config['useProxy']) -> None:
        self._use_proxy = use_proxy

    def _applyProxy(self, session: tls_client.Session) -> None:
        if self._use_proxy:
            proxies = loadProxies()
            randproxy = random.choice(proxies)
            session.proxies = {
                "http": f"http://{randproxy}",
                "https": f"http://{randproxy}"
            }

    def session(self, update_headers: dict = {}) -> tls_client.Session:
        spoof = random.choice(available_browser_spoof)

        session = tls_client.Session(
            client_identifier=spoof['client_identifier'],  # Browser fingerprint for mimicking a browser
            random_tls_extension_order=True  # Randomize TLS extension order for added realism
        )
        self._applyProxy(session)
        session.headers = {
            "User-Agent": spoof['user_agent']
        }
        session.headers.update(update_headers)
        return session