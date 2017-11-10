#! /usr/bin/env python3
# copyright@mathu
# Author: Ruimin Wang, ruimin.wang13@gmail.com
# Func: the basic parser class for common spider


from ..utils.basic_definition import *
from ..utils.exception import *
from ..loader.basic_loader import BasicLoader
import logging
import re

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


