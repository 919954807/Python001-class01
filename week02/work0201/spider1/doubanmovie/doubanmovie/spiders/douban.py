
import scrapy
#from bs4 import BeautifulSoup
from doubanmovie.items import DoubanmovieItem
from scrapy.selector import Selector

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    
    #爬虫启动前执行
    def start_requests(self):
        for i in range(0,1):
            url = f'https://movie.douban.com/top250?start={i*25}'
            #对取到的每一个页面发起一个请求
            yield scrapy.Request(url=url,callback=self.parse)    

    def parse(self, response):
        #soup = BeautifulSoup(response.text,'html.parser')
        #title_list = soup.find_all('div',attrs={'class':'hd'})
        movies = Selector(response=response).xpath('//div[@class="hd"]')
        #print(movies)
        for i in movies:
            item = DoubanmovieItem()
            title = i.xpath('./a/span/text()')
            link = i.xpath('./a/@href')  
            #print("---------------link-----------------")
            #print(link)
            #print("--------------link.extract_first().strip------------------")
            #print(link.extract_first().strip())  
            item['title'] = title.extract_first().strip()
            url = link.extract_first().strip()
            item['link'] = url
            #print("---------------item-----------------")
            #print(item)
            yield scrapy.Request(url=url,meta={'item':item},callback=self.parse2)

    def parse2(self,response):
        item = response.meta['item']
        print("---------------parse2-----------------")
        contents = Selector(response=response).xpath('//div[@class="indent"]')
        #print("---------------contents-----------------")
        #print(contents)
        temp = contents.xpath('./span/text()')
        # print(temp)
        content = temp.extract_first().strip()
        item['content'] = content
        yield item  