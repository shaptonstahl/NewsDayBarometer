"""
resolve url shorteners to where they eventually point
"""

import re
import httplib


def split_url_to_host_and_path(url):
    try:
        url = re.search("https{0,1}:\/\/(.*)", url).group(1)
        if len(re.findall("\/", url)) == 0:
            url = url + "/"
        host = re.match("([^\/]*)\/.*", url).group(1)
        path = re.search("[^\/]*(\/.*$)", url).group(1)
    except:
        return None
    return host, path


def probe_url(url):
    host, path = split_url_to_host_and_path(url)
    conn = httplib.HTTPConnection(host)
    conn.request("HEAD", path)
    res = conn.getresponse()
    conn.close()
    return res


def unshorten_url(url, max_redirects=3):
    n_redirects = 0
    try:
        res = probe_url(url)
        while re.match("3", str(res.status)):
            n_redirects += 1
            try:
                redirected_url = [x[1] for x in res.getheaders() if x[0] == "location"][
                    0
                ]
                if re.match("\/", redirected_url):
                    url = (
                        re.match("(https{0,1}:\/\/)", url).group(1)
                        + split_url_to_host_and_path(url)[0]
                        + redirected_url
                    )
                else:
                    url = redirected_url
                res = probe_url(url)
            except:
                break
            if n_redirects >= max_redirects:
                break
        return url.strip()
    except:
        return None
