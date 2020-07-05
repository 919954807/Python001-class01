# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import doubanmovie.settings as settings
import pymysql

class DoubanmoviePipeline:
    def __init__(self):
    # 连接数据库
        self.connect = pymysql.connect(
        host=settings.MYSQL_HOST,
        db=settings.MYSQL_DBNAME,
        user=settings.MYSQL_USER,
        passwd=settings.MYSQL_PASSWD,
        charset='utf8')
    # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()


    def process_item(self, item, spider):
        print("----------process_item----------")
        title = item['title']
        link = item['link']
        content = item['content']
        output = f'|{title}| \t|{link}|\t |{content}|\n\n'
        #print("---------------#######--process_item--##########--------------------------")
        #print(output)

        #写入文件
        with open('./doubanmovie.txt','a+',encoding='utf-8') as article:
            print("打印")
            article.write(output)
        
        #写入数据库,插入数据库后目前显示乱码。。。xampp中
        try:
            # 插入数据
            self.cursor.execute(
                """insert into filmtable(title,link, content)
                value (%s, %s, %s)""",
                (item['title'],
                 item['link'],
                 item['content']))
            # 提交sql语句
            self.connect.commit()
        except Exception as e:
            print("错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")

        return item

