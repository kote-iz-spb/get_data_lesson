# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhSpiderSpider(scrapy.Spider):
    name = 'hh_spider'
    allowed_domains = ['hh.ru']

    def __init__(self,vacancy):
        self.start_urls = [f'https://spb.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text={vacancy}&L_save_area=true&area=113&from=cluster_area&showClusters=true']

    def parse(self, response:HtmlResponse):
        next_page=response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)
        vac_links=response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        for link in vac_links:
            yield response.follow(link,callback=self.pp)



    def pp(self,response:HtmlResponse):
        name=response.xpath("//h1[@data-qa='vacancy-title']//text()").extract_first()
        author=response.xpath("//a[@data-qa='vacancy-company-name']//text()").extract()
        salary=response.xpath("//p[@class='vacancy-salary']//text()").extract()
        city=response.xpath("//p[@data-qa='vacancy-view-location']/text()").extract()
        link=response.url

        yield JobparserItem(name=name,author=author,salary=salary,city=city,link=link)


