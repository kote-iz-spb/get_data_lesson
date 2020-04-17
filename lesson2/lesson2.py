import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re

vacancy1='android'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'}
vacancy_all = []

# Обработка вакансий HH.ru

hh_link='https://spb.hh.ru'
page=f'/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text={vacancy1}&page=0'

while True:
    response=requests.get(hh_link+page,headers=headers).text
    soup=bs(response,'lxml')
    vacancy_list=soup.find('div',{'class':'vacancy-serp'})

    sep_vacancy=vacancy_list.find_all('div',{'class':'vacancy-serp-item'})


    for vacancy in sep_vacancy:
        vacancy_data={}
        vacancy_link=vacancy.find('a')['href']
        vacancy_name=vacancy.find('a').get_text()
        vacancy_descr=vacancy.find('div',{'data-qa':'vacancy-serp__vacancy_snippet_responsibility'}).find_parent().get_text()
        vacancy_price=vacancy.find('div',{'class':'vacancy-serp-item__sidebar'}).get_text().replace('\xa0','')

        salary_min=re.findall('от\s(\d+)\s',vacancy_price)
        salary_max=re.findall('до\s(\d+)\s',vacancy_price)
        currency=re.findall('\s([а-я]+|[A-Z]+)',vacancy_price)

        if len(salary_max)==0:
            salary_max=re.findall('-(\d+)',vacancy_price)
            if len(salary_max)==0:
                salary_max =[0]
        if len(salary_min)==0:
            salary_min=re.findall('(\d+)-',vacancy_price)
            if len(salary_min) == 0:
                salary_min = [0]


        vacancy_data['name']=vacancy_name
        vacancy_data['link']=vacancy_link
        vacancy_data['descr']=vacancy_descr
        vacancy_data['salary_min']=int(salary_min[0])
        vacancy_data['salary_max']=int(salary_max[0])
        vacancy_data['vacancy_price']=vacancy_price
        vacancy_data['currency'] = currency
        vacancy_all.append(vacancy_data)


    try:
        button=soup.find('a',{'data-qa':'pager-next'})['href']
        page=button
    except TypeError:
        break

print(len(vacancy_all))
# Обработка вакансий Superjob
superjob_link='https://russia.superjob.ru'
page=f'/vacancy/search/?keywords={vacancy1}'

while True:
        response=requests.get(superjob_link+page,headers=headers).text
        soup=bs(response,'lxml')

        vacancy_list=soup.find('div',{'class':'_1ID8B'})

        sep_vacancy=vacancy_list.find_all('div',{'class':'_3zucV f-test-vacancy-item _3j3cA RwN9e _3tNK- _1NStQ _1I1pc'})

        for sep_vacancy in sep_vacancy:
                vacancy_data={}
                vacancy_link=sep_vacancy.find('a')['href']
                vacancy_name=sep_vacancy.find('a').get_text()
                vacancy_descr=sep_vacancy.find('div',{'class':'_3cLIl _3C76h _10Aay _2_FIo _1tH7S'}).get_text()
                vacancy_price=sep_vacancy.find('span',{'class':'_3mfro _2Wp8I _31tpt f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).get_text().replace('\xa0','')

                #vacancy_name1=sep_vacancy.find('a').find_parent().find_parent().find_parent().get_text()


                salary_min=re.findall('от(\d+)',vacancy_price)
                salary_max=re.findall('до(\d+)',vacancy_price)
                currency=re.findall('\d+([а-я]+|[A-Z]+)',vacancy_price)

                if len(salary_max)==0:
                        salary_max=re.findall('.*—(\d+)',vacancy_price)
                        if len(salary_max)==0:
                                salary_max =[0]
                if len(salary_min)==0:
                        salary_min=re.findall('(\d+)—.*',vacancy_price)
                        if len(salary_min) == 0:
                                salary_min = [0]

                vacancy_data['name']=vacancy_name
                vacancy_data['link']=vacancy_link
                vacancy_data['descr']=vacancy_descr
                vacancy_data['salary_min']=int(salary_min[0])
                vacancy_data['salary_max']=int(salary_max[0])
                vacancy_data['vacancy_price']=vacancy_price
                vacancy_data['currency'] = currency
                vacancy_all.append(vacancy_data)

        try:
                button = soup.find('a', {'rel': 'next'})['href']
                page = button
        except TypeError:
                break


print(len(vacancy_all))
#pprint(vacancy_all)
