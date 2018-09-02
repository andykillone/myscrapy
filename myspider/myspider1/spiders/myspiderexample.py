# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: myspiderexample.py
@time: 2018/08/18 12:44
"""

import scrapy
from myspider1.items import MyspiderItem
import json
from urllib.parse import urljoin
import time

class myspider1(scrapy.Spider):

    name = "myspider"
    offset = 1


    def start_requests(self):

        with open("log4.txt", "a+", encoding="utf-8") as f:
            f.write(time.ctime() + '*'*80 + '\r\n')
        # 定义爬取的链接
        urls =["https://cd.ke.com/ershoufang/jinjiang/"]

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

        item = MyspiderItem()
        titles = response.xpath('//div[@class="info clear"]/div[1]/a/text()').extract()
        prices = response.xpath('//div[@class="priceInfo"]/div[1]/span/text()').extract()
        unitprices = response.xpath('//div[@class="unitPrice"]/span/text()').extract()
        housenames = response.xpath('//div[@class="info clear"]/div[2]/div/a/text()').extract()
        houseinfos = response.xpath('//div[@class="houseInfo"]/text()').extract()
        district = response.xpath('//a[@class="selected CLICKDATA"]/text()').extract_first()
        # with open("houses.txt", "w",encoding="utf-8") as f:
        for title, price, unitprice, housename, houseinfo in zip(titles, prices, unitprices, housenames, houseinfos):
            self.log(title + price + unitprice + housename + houseinfo)
            item["title"] = title.strip()
            item["price"] = float(price.strip())
            item["unitprice"] = unitprice.strip()
            item["housename"] = housename.strip()
            item["houseinfo"] = houseinfo.strip()
            item["houseinfo"] = houseinfo.strip()
            item["district"] = district.strip()
            yield item

        gettotalpage = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract_first()
        pagejson = json.loads(gettotalpage)
        totalpage = pagejson["totalPage"]
        curPage = pagejson["curPage"]
        next_temp = response.xpath('//a[@class="selected CLICKDATA"]/@href').extract_first()

        if curPage == 1:
            newurl = response.urljoin(next_temp + "pg" + str(curPage))
            with open("log4.txt", "a+", encoding="utf-8") as f:
                f.write(newurl + '\r\n')
            for page in range(curPage,totalpage):
                newurl = response.urljoin(next_temp + "pg" + str(page+1))
                with open("log4.txt","a+",encoding="utf-8") as f:
                    f.write(newurl+'\r\n')
                yield scrapy.Request(newurl, callback=self.parse)
        elif curPage == totalpage:
            self.offset += 1
            with open("log4.txt", "a+", encoding="utf-8") as f:
                f.write("offset:"+ str(self.offset) + '\r\n')
            next_temp = response.xpath(
                "/html/body/div[3]/div[1]/dl[2]/dd/div[1]/div[1]/a[%s]/@href" % self.offset).extract_first()
            if next_temp:
                url = urljoin("https://cd.ke.com/ershoufang", next_temp)
                self.log("start to get :" + url)
                yield scrapy.Request(url, callback=self.parse)
