# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: myspiderexample.py
@time: 2018/08/18 12:44
"""

import scrapy


class myspider1(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "myspider"  # 定义蜘蛛名

    def start_requests(self):  # 由此方法通过下面链接爬取页面

        # 定义爬取的链接
        urls =['https://cd.ke.com/ershoufang/pg2/']
        # url1 = 'https://www.guazi.com/cd/q3jinkou/o1/#bread'
        # for i in range(10):
        #     urls.append(url1+str(i))
        # print(urls)
        # urls = [
        #     'http://lab.scrapyd.cn/page/1/',
        #     'http://lab.scrapyd.cn/page/2/',
        # ]
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Cookie": "lianjia_uuid=794795bd-30bf-482d-b559-e73a5421b782; select_city=510100; lianjia_ssid=99470c01-700d-4966-9c4a-745cb94b94d2; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1535773358; gr_user_id=86bef8ab-ced0-4ad4-a0e0-c60ce4d66a07; _smt_uid=5b8a0aad.57a06733; sajssdk_2015_cross_new_user=1; Hm_lvt_9d483e9e48ba1faa0dfceaf6333de846=1535773358; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221659339b7a2a15-0f06dc55d536f-30584d74-2073600-1659339b7a39d1%22%2C%22%24device_id%22%3A%221659339b7a2a15-0f06dc55d536f-30584d74-2073600-1659339b7a39d1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22tencent%22%2C%22%24latest_utm_medium%22%3A%22navi%22%2C%22%24latest_utm_campaign%22%3A%22pc%22%2C%22%24latest_utm_content%22%3A%222018615%22%2C%22%24latest_utm_term%22%3A%22mingzhan%22%7D%7D; gr_session_id_a1a50f141657a94e=a9d1f33d-173c-43cf-922a-72ac94b3ad2e; gr_session_id_a1a50f141657a94e_a9d1f33d-173c-43cf-922a-72ac94b3ad2e=true; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1535775280; Hm_lpvt_9d483e9e48ba1faa0dfceaf6333de846=1535775281",
            "Host":"cd.ke.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5773.400 QQBrowser/10.2.2059.400"
        }

        for url in urls:
            yield scrapy.Request(url=url, headers=header,callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理


    def parse(self, response):
        '''
        start_requests已经爬取到页面，那如何提取我们想要的内容呢？那就可以在这个方法里面定义。
        这里的话，并木有定义，只是简单的把页面做了一个保存，并没有涉及提取我们想要的数据，后面会慢慢说到
        也就是用xpath、正则、或是css进行相应提取，这个例子就是让你看看scrapy运行的流程：
        1、定义链接；
        2、通过链接爬取（下载）页面；
        3、定义规则，然后提取数据；
        就是这么个流程，似不似很简单呀？
        '''
        # page = response.url.split("/")[-2]  # 根据上面的链接提取分页,如：/page/1/，提取到的就是：1
        # print(response.url.split("/"))
        # print("response is ::",response)
        # print("response body is :::",response.url, response.body.decode('utf-8'))
        # filename = 'myspider1-%s.html' % page  # 拼接文件名，如果是第一页，最终文件名便是：mingyan-1.html
        # with open(filename, 'wb') as f:  # python文件操作，不多说了；
        #     f.write(response.body)  # 刚才下载的页面去哪里了？response.body就代表了刚才下载的页面！
        # self.log('保存文件: %s' % filename)  # 打个日志

        titles = response.xpath("/html/body/div[4]/div[1]/ul//li/div[1]/div[1]/a/text()").extract()
        prices = response.xpath("/html/body/div[4]/div[1]/ul//li/div[1]/div[6]/div[1]/span/text()").extract()
        unitprices = response.xpath("/html/body/div[4]/div[1]/ul/li/div[1]/div[6]/div[2]/span/text()").extract()
        housenames = response.xpath("/html/body/div[4]/div[1]/ul/li/div[1]/div[2]/div/a/text()").extract()
        houseinfos = response.xpath("/html/body/div[4]/div[1]/ul/li/div[1]/div[2]/div/text()").extract()
        with open("houses.txt", "w",encoding="utf-8") as f:
            for title, price, uniprice, housename, houseinfo in zip(titles, prices, unitprices, housenames, houseinfos):
                self.log(title + price + uniprice + housename + houseinfo)
                f.write(title+"\r\n")
                f.write("---" + price+"\r\n")
                f.write("---" + uniprice+"\r\n")
                f.write("---" + housename+"\r\n")
                f.write("---" + houseinfo+"\r\n")
