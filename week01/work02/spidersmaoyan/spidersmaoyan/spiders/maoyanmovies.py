import scrapy
from scrapy.selector import Selector
from spidersmaoyan.items import SpidersmaoyanItem

class MaoyanmoviesSpider(scrapy.Spider):
    name = 'maoyanmovies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    # 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象（Request）。
    # start_requests()方法读取start_urls列表中的URL并生成Request对象，发送给引擎。
    # 引擎再指挥其他组件向网站服务器发送请求，下载网页
    def start_requests(self):
        print("-------------开始执行方法：start_requests-------------------------")
        for i in range(0,1):
            url = f'https://maoyan.com/films?showType=3&offset={i*30}'
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        print("-------------开始执行方法：parse-------------------------")
        print(response.url)
        #此处的xpath选择影片的标签
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]')
        print("-------------打印movies-------------------------")
        print(movies)
        for i in range(0,10):
            print("-------------第一个parse的for循环-------------------------")
            link = movies[i].xpath('./a/@href')
            print("-------------打印link-------------------------")
            print(link)
            # link中包含的串要过滤掉
            real_link = 'https://maoyan.com'+str(link.extract_first().strip())
            print("-------------打印real_link-------------------------")
            print(real_link)
            item = SpidersmaoyanItem()
            yield scrapy.Request(url=real_link,meta={'item':item},callback=self.parse2)

    def parse2(self, response):
        #详情页取定义存数据的item
        item = response.meta['item']
        #通过url取数据
        movies = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        
        #将取到的数据依次存入item
        for movie in movies:
            filmtitle = movie.xpath('./h1/text()')
            
            
            #filmtype不定，有多个，用循环取,暂未实现
            filmtypes = Selector(response=response).xpath('//li[@class="ellipsis"]')
            print("-------------打印filmtypes-------------------------")
            print(filmtypes)
            filmtypestr = ' '
            for filmtype in filmtypes:
                print("-------------打印filmtype-------------------------")
                print(filmtype)
                i = filmtypes.index(filmtype)
                #print("i:" + str(i))
                tempstr = filmtype.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a[1]/text()').extract_first().strip()
                print("-------------打印tempstr-------------------------")
                print(tempstr)
                filmtypestr.join(tempstr)
            print("-------------打印filmtypesstr-------------------------")
            print(filmtypestr)
            

            #filmtype只取了一个
            filmtype = movie.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a[1]/text()')
            filmdate = movie.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()')
            #打印调试
            print("-------------------打印parse2中item的各项---------------------------")
            print(filmtitle.extract_first().strip())
            print(filmtype.extract_first().strip())
            print(filmdate.extract_first().strip())
            #传入值
            item['filmtitle'] = filmtitle.extract_first().strip()
            item['filmtype'] = filmtype.extract_first().strip()
            item['filmdate'] = filmdate.extract_first().strip()
        #返回数据      
        yield item
