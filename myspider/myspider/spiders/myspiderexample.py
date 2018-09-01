# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: myspiderexample.py
@time: 2018/08/18 12:44
"""

import scrapy
import myspider.items


class myspider1(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "myspider123"  # 定义蜘蛛名

    def start_requests(self):  # 由此方法通过下面链接爬取页面

        # 定义爬取的链接
        count = 20
        # urls =[]
        urls = ['https://www.bilibili.com/v/music/original/#/all/default/0/{}/'.format(str(i)) for i in range(count)]
        # for i in range(10):
        #     urls.append(url1+str(i))
        # print(urls)
        # urls = [
        #     'http://lab.scrapyd.cn/page/1/',
        #     'http://lab.scrapyd.cn/page/2/',
        # ]
        for u in urls:
            print(u)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理


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
        item = myspider.items.MyspiderItem()
        titles = response.xpath("//*[@id=\"videolist_box\"]/div[2]/ul/li/div/div[2]/a/text()")
        for i in titles:
            print(i)
        exit()

