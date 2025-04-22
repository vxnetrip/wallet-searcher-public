# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


import asyncio
import httpx
import time
import re

from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, method: str, _url: str) -> None:
        self.method = method
        self._url = _url

    def get_url(self, **kwargs):
        return self._url.format(**kwargs, method=self.method)

    async def get_response(self, client: httpx.AsyncClient):
        return await client.get(self.get_url())
    
    async def handle(self, response: httpx.Response):
        return response.text
    
    async def scrape(self, client: httpx.AsyncClient):
        response = await self.get_response(client)
        proxies = await self.handle(response)
        pattern = re.compile(r"\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})?")
        return re.findall(pattern, proxies)


# spys.me
class SpysMeScraper(Scraper):
    def __init__(self, method: str) -> None:
        super().__init__(method, "https://spys.me/{mode}.txt")
    
    def get_url(self, **kwargs):
        mode = "proxy" if self.method == "http" else "socks" if self.method == "socks" else "unknown"
        if mode == "unknown":
            raise NotImplementedError
        return super().get_url(mode=mode, **kwargs)
    

# proxyscrape.com
class ProxyScrapeScraper(Scraper):
    def __init__(self, method: str, timeout: int = 1000, country: str = "All") -> None:
        self.timeout = timeout
        self.country = country
        super().__init__(method,
                         "https://api.proxyscrape.com/?request=getproxies"
                         "&proxytype={method}"
                         "&timeout={timout}"
                         "&country={country}")
        
    def get_url(self, **kwargs):
        return super().get_url(timeout=self.timeout, country=self.country, **kwargs)
    

# geonode.com
# class GeoNodeScraper(Scraper):
#     def __init__(self, method: str, limit: str = "500", page: str = "1", sort_by: str = "lastChecked", sort_type: str = "desc") -> None:
#         self.limit = limit
#         self.page = page
#         self.sort_by = sort_by
#         self.sort_type = sort_type
#         super().__init__(method,
#                          "https://proxylist.geonode.com/api/proxy-list?"
#                          "&limit={limit}"
#                          "&page={page}"
#                          "&sort_by={sort_by}"
#                          "&sort_type={sort_type}")
        


# From proxy-list.download
class ProxyListDownloadScraper(Scraper):

    def __init__(self, method, anon):
        self.anon = anon
        super().__init__(method, "https://www.proxy-list.download/api/v1/get?type={method}&anon={anon}")

    def get_url(self, **kwargs):
        return super().get_url(anon=self.anon, **kwargs)


# For websites using table in html
class GeneralTableScraper(Scraper):

    async def handle(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        proxies = set()
        table = soup.find("table", attrs={"class": "table table-striped table-bordered"})
        for row in table.findAll("tr"):
            count = 0
            proxy = ""
            for cell in row.findAll("td"):
                if count == 1:
                    proxy += ":" + cell.text.replace("&nbsp;", "")
                    proxies.add(proxy)
                    break
                proxy += cell.text.replace("&nbsp;", "")
                count += 1
        return "\n".join(proxies)


# For websites using div in html
class GeneralDivScraper(Scraper):

    async def handle(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        proxies = set()
        table = soup.find("div", attrs={"class": "list"})
        for row in table.findAll("div"):
            count = 0
            proxy = ""
            for cell in row.findAll("div", attrs={"class": "td"}):
                if count == 2:
                    break
                proxy += cell.text+":"
                count += 1
            proxy = proxy.rstrip(":")
            proxies.add(proxy)
        return "\n".join(proxies)

    def get_url(self, **kwargs):
        return super().get_url(limit=self.limit, page=self.page, sort_by=self.sort_by, sort_type=self.sort_type, **kwargs)


# For scraping live proxylist from github
class GitHubScraper(Scraper):
        
    async def handle(self, response):
        tempproxies = response.text.split("\n")
        proxies = set()
        for prxy in tempproxies:
            if self.method in prxy:
                proxies.add(prxy.split("//")[-1])

        return "\n".join(proxies)




scrapers = [
    SpysMeScraper("http"),
    # SpysMeScraper("socks"),
    ProxyScrapeScraper("http"),
    # ProxyScrapeScraper("socks4"),
    # ProxyScrapeScraper("socks5"),
    # GeoNodeScraper("socks"),
    ProxyListDownloadScraper("https", "elite"),
    ProxyListDownloadScraper("http", "elite"),
    ProxyListDownloadScraper("http", "transparent"),
    ProxyListDownloadScraper("http", "anonymous"),
    GeneralTableScraper("https", "http://sslproxies.org"),
    GeneralTableScraper("http", "http://free-proxy-list.net"),
    GeneralTableScraper("http", "http://us-proxy.org"),
    # GeneralTableScraper("socks", "http://socks-proxy.net"),
    GeneralDivScraper("http", "https://freeproxy.lunaproxy.com/"),
    GitHubScraper("http", "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"),
    # GitHubScraper("socks4", "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"),
    # GitHubScraper("socks5", "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"),
    GitHubScraper("http", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt"),
    # GitHubScraper("socks", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt"),
    GitHubScraper("https", "https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt"),
    GitHubScraper("http", "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt"),
    # GitHubScraper("socks4", "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt"),
    # GitHubScraper("socks5", "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt"),
    GitHubScraper("http", "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt"),
    GitHubScraper("http", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"),
    GitHubScraper("http", "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt")
    
]




async def scrape(method, output):
    now = time.time()

    print("Scraping proxies...")

    proxies = []
    tasks = []
    client = httpx.AsyncClient(follow_redirects=True)

    async def scrape_scraper(scraper: Scraper):
        try:
            print(f"[ {scraper.get_url()} ] Scraping...")
            proxies.extend(await scraper.scrape(client))
        except:
            pass


    
    for scraper in scrapers:
        tasks.append(asyncio.ensure_future(scrape_scraper(scraper)))



    await asyncio.gather(*tasks)
    await client.aclose()

    proxies = set(proxies)

    print(f"Writing {len(proxies)} proxies to file...")
    with open(output, "w") as f:
        f.write("\n".join(proxies))

    print(f"Done in {time.time() - now} seconds.")



def run_scraper():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape("http", "./input/scraped_http.txt"))
    loop.close()


if __name__ == "__main__":
    run_scraper()