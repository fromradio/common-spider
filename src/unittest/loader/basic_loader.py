

from ...loader.basic_loader import BasicLoader


def main():
    content = BasicLoader.load_url("http://www.baidu.com", None, None, 200, 500, 4)
    print(content)

if __name__ == '__main__':
    main()
