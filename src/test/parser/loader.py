
from ...parser import basic_parser


def main():
    text = basic_parser.BasicLoader.load_url("http://www.baidu.com", None, None, 200, 500, 5)
    print(text)

if __name__ == '__main__':
    main()
