#! /usr/bin/env python3
# copyright@mathu
# Author: Ruimin Wang, ruimin.wang13@gmail.com
# Func: the basic parser class for common spider


from ..utils.basic_definition import *
from ..utils.exception import *
import requests
import logging
import re

class BasicLoader(object):
    @staticmethod
    def load_url(url, data, header, timeout, time_interval, num_retries):
        for _ in range(num_retries):
            if timeout >= 0:
                try:
                    if data:
                        req = request.get(url, data=data, headers=header, timeout=timeout)
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

class BasicParser(object):
    def __init__(self,
                time_interval,
                num_retries,
                timeout,
                data=None,
                header=None,
                logger=None):
        self.time_interval = time_interval
        self.num_retries = num_retries
        self.timeout = timeout
        self.header = header
        if not logger:
            logging.basicConfig(format=FORMAT)
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
        self.data = data
        self.content = None

    def read_from_url(self, url, reg):
        self.content = BasicLoader().load_url(url, self.data, self.header, self.timeout,
                self.time_interval, self.num_retries)
        self.read_content(reg)
    def read_content(self, reg):
        if not self.content:
            raise ParserException("Content is None")
        print(self.content)
        return re.findall(reg, self.content, re.S)


