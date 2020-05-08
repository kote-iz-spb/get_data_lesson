# -*- coding: utf-8 -*-
from pymongo import MongoClient

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base=client.vacancy_list


    def process_item(self, item, spider):
        if spider.name=='hh_spider':
            item['author']=''.join(item['author']).replace('\xa0',' ')
            item['salary']=''.join(item['salary']).replace('\xa0','')
            item['salary_min'] = re.findall('от\s(\d+)\s', item['salary'])
            item['salary_max'] = re.findall('до\s(\d+)\s', item['salary'])
            item['currency'] = re.findall('\s([а-я]+|[A-Z]+)', item['salary'])
            item['currency'] = ' '.join(item['currency'])
            item['currency'] = re.findall('(руб|[A-Z]+)', item['currency'])
            item['city']=item['city']

        else:
            item['author']=item['author']
            item['city'] = item['city']
            item['salary'] = ' '.join(item['salary']).replace('\xa0', '')
            item['salary_min'] = re.findall('от\s+(\d+)', item['salary'])
            item['salary_max'] = re.findall('до\s+(\d+)', item['salary'])
            if len(item['salary_max']) == 0:
                item['salary_max'] = re.findall('\s(\d+)\s', item['salary'])
                if len(item['salary_max']) == 0:
                    item['salary_max'] = [0]
            if len(item['salary_min']) == 0:
                item['salary_min'] = re.findall('^(\d+)\s', item['salary'])
                if len(item['salary_min']) == 0:
                    item['salary_min'] = [0]
            item['currency'] = re.findall('(руб|[A-Z]+)', item['salary'])

        vacancy_y=self.mongo_base[spider.name]
        vacancy_y.insert_one(item)


        return item
