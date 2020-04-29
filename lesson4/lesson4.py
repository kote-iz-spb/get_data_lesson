import requests
from pprint import pprint
from pymongo import MongoClient
from lxml import html
import re
from datetime import datetime

current_date = str(datetime.now().date())

headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

yandex_link='https://yandex.ru'
mail_link='https://news.mail.ru'

response = requests.get(mail_link, headers=headers)
string = html.fromstring(response.text)
news2=string.xpath("//li[contains(@class,'list__item')]/a[contains(@class,'list__text')]/@href")

news=[]
for new in news2:
    item={}
    link=mail_link+new
    response2=requests.get(link, headers=headers)
    string2=html.fromstring(response2.text)
    author=string2.xpath("//span[@class='note']//span[@class='link__text']/text()")
    item['author']=author[0]
    datetime=string2.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
    description=string2.xpath("//h1[@class='hdr__inner']/text()")
    item['description']=description[0]
    item['link']=link+new
    datetime=str(datetime)
    date=re.findall('(\d.+)T',datetime)
    time=re.findall('T(\d+:\d+)',datetime)
    item['date'] = date[0]
    item['time']=time[0]
    news.append(item)


lenta_link='https://lenta.ru'
response_lenta = requests.get(lenta_link, headers=headers)
string_lenta = html.fromstring(response_lenta.text)
news3=string_lenta.xpath("//div[@class='item']/a/@href")
news6=[]
for n in news3:
    new=re.findall('/news/\d.+',n)
    if len(new)>0:
        news6.append(new[0])

for new in news6:
    item = {}
    link=lenta_link+new
    response2 = requests.get(link, headers=headers)
    string2 = html.fromstring(response2.text)
    author='lenta.ru'
    description = string2.xpath("//h1[@class='b-topic__title']/text()")
    datetime=string2.xpath("//div[@class='b-topic__info']/time/@datetime")
    datetime = str(datetime)
    date=re.findall('(\d.+)T',datetime)
    time=re.findall('T(\d+:\d+)',datetime)

    item['author'] = author
    item['date'] = date[0]
    item['time']=time[0]
    item['description'] = description[0]
    item['link']=link+new
    news.append(item)


response_yandex = requests.get(yandex_link+'/news', headers=headers)
string_yandex = html.fromstring(response_yandex.text)
news4=string_yandex.xpath("//h2[@class='story__title']/a/@href")
news5=string_yandex.xpath("//td[@class='stories-set__item']")

for new in news5:
    item = {}
    search_link=new.xpath(".//h2[@class='story__title']/a/@href")
    link=yandex_link+search_link[0]
    description = new.xpath(".//h2[@class='story__title']/a/text()")
    author_date=new.xpath(".//div[@class='story__date']/text()")
    author=re.findall('(\S+)\s',author_date[0])
    time=re.findall('\s(\d+:\d+)',author_date[0])

    item['time']=time[0]
    item['author'] = author[0]
    item['description'] = description[0]
    item['link'] = link
    item['date'] = current_date
    news.append(item)

pprint(news)

