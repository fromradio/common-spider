#! /usr/bin/env python
# copyright@mathu
# Author: Ruimin Wang, wangruimin@qiyi.com
# Func: test for the loader package


from ...loader.basic_loader import *


def main():
    loader = BasicLoader(500, 200, 5)
    print loader.load("http://www.baidu.com")
    pass


if __name__ == '__main__':
    main()

