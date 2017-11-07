

from ...parser.basic_parser import *

def main():
    parser = BasicParser(500, 5, 200)
    res = parser.read_from_url("http://www.baidu.com", "<div>*</div>")
    print res

if __name__ == '__main__':
    main()
