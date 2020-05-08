# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjSpiderSpider(scrapy.Spider):
    name = 'sj_spider'
    allowed_domains = ['russia.superjob.ru']

    def __init__(self,vacancy1):
        self.start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={vacancy1}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy_links = response.xpath("//div[@class='_3zucV f-test-vacancy-item _3j3cA RwN9e _3tNK- _1NStQ _1I1pc']//a[@target='_blank']/@href").extract()

        for link in vacancy_links:
            yield response.follow(link,callback=self.qq)



    def qq(self,response:HtmlResponse):
        name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract_first()
        author = response.xpath("//div[@class='_2g1F-']/div[@class='_3zucV undefined']//text()").extract_first()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        city = response.xpath("//div[@class='f-test-address _3AQrx']//text()").extract()
        link = response.url

        yield JobparserItem(name=name, author=author, salary=salary, city=city, link=link)

