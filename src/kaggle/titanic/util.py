from urllib import request, parse
import re


def get_hops(url):
    meta_redirects = re.compile('<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)
    hops = []

    while url:
        if url in hops:
            url = None
        else:
            hops.insert(0, url)

            req = request.Request(
                url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            resp = request.urlopen(req)
            if resp.url != url:
                hops.insert(0, resp.url)
            match = meta_redirects.search(resp.read().decode('utf-8'))
            if match:
                url = parse.urljoin(url, match.groups()[0].strip())
            else:
                url = None
    return hops


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def utf8_ascii(a, id=True):
    if not id:
        return a.encode('ascii', 'ignore').decode('ascii')
    else:
        return a
