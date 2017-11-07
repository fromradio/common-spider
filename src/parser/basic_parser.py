#! /usr/bin/env python3
# copyright@mathu
# Author: Ruimin Wang, ruimin.wang13@gmail.com
# Func: the basic parser class for common spider


class BasicParser(object):
    def __init__(self,
                time_interval,
                num_retries,
                header=None,
                logger=None):
        self.time_interval = time_interval
        self.num_retries = num_retries
        if header is None:
            pass
        else:
            self.header = header
        self.content = None
    def load_url(self, url):
        pass
    def read_content(self, content):
        pass

