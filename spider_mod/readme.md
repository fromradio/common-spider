### webparse.py

* parse, parse_post, gethtml都是用requests的方式解析网页.
* return中的info是记录网页获取是否正确的，info>=0表示获取正常
* Driver 是使用selenium的类，包含一系列如click, send_keys, parse等方法

### writefile.py

* writerow是将list类型以add的模式写入txt文件
* writecsv是将list类型以add的模式写入csv文件

### mysql.py

* 实现了用python对mysql的操作, 主要包括建表, 查询, 插入, 执行语句等功能

### clear.py

* 以前师兄师姐写的包, 主要是清洗爬下来带有乱码等的数据

### club_autohome.py

* 汽车论坛的示例程序，展示如何调用这些包