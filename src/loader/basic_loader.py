#! /usr/bin/env python3
# copyright@mathu
# Author: Ruimin Wang, wangruimin@qiyi.com
# Func: basic loader for common spider

from ..utils.exception import LoaderException
import requests

class BasicLoader(object):
    @staticmethod
    def load_url(url, data, header, timeout, time_interval, num_retries):
        for _ in range(num_retries):
            if timeout >= 0:
                try:
                    if data:
                        req = requests.get(url, data=data, headers=header, timeout=timeout)
                    else:
                        req = requests.get(url, headers=header, timeout=timeout)
                except Exception:
                    continue
            else:
                try:
                    if data:
                        req = requests.get(url, data=data, headers=header)
                    else:
                        req = requests.get(url, headers=header)
                except Exception:
                    continue
            if req:
                if not req.url.strip("\\/") == url.strip("\\/"):
                    raise LoaderException("error: url has changed from {} to {}".format(url, req.url))
                else:
                    return req.text
            pass
        raise LoaderException("retry time exceeds {}".format(num_retries))

