# fang
链家爬虫
python版本>3.5

先输入：
git clone https://github.com/DevXXM/fang.git

然后
cd fang

pip install -r requirements.txt

等待安装成功之后
把fang.sql文件导入到mysql
去settings.py配置好mysql

然后改一下spiders/lianjia.py
把city改为自己要爬的城市，urls里面的链接改为自己要爬城市的链家地址

比如重庆：https://cq.lianjia.com/xiaoqu
武汉：https://wh.lianjia.com/xiaoqu
深圳：https://sz.lianjia.com/xiaoqu


最后输入命令：scrapy crawl  lianjia  即可启动
