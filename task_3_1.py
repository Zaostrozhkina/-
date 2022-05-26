# https://spb.hh.ru/search/vacancy?employment=full&experience=between1And3&label=not_from_agency&schedule=fullDay&schedule=remote&search_field=name&search_field=company_name&search_field=description&only_with_salary=true&text=data+analyst&order_by=relevance&search_period=0&items_on_page=50&no_magic=true&L_save_area=true&customDomain=1

from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient
from pprint import pprint


# with open('vacancies.json', 'r') as f:
#     vacancy_list = json.load(f)

client = MongoClient('127.0.0.1', 27017)
db = client['bd_hh']
vacancy_hh = db.vacancy_hh
# vacancy_hh.insert_many(vacancy_list)


main_url = 'https://spb.hh.ru'
params = {'employment': 'full',
          'experience': 'between1And3',
          'label': 'not_from_agency',
          'schedule':  ['fullDay', 'remote'],
          'search_field': ['name', 'company_name', 'description'],
          'only_with_salary': 'true',
          'text': 'data analyst',
          'order_by': 'relevance',
          'search_period': 0,
          'items_on_page': 19,
          'no_magic': 'true',
          'L_save_area': 'true',
          'customDomain': 1,
          'page': 0}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}
response = requests.get(main_url+'/search/vacancy', params=params, headers=headers)

soup = bs(response.text, 'html.parser')

last_page = soup.find_all('span', {'class': 'pager-item-not-in-short-range'})[-1].text
last_page = int(last_page)

for i in range(last_page):

    response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')

    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})[1:]

    for vacancy in vacancies:
        vacancy_info = {}

        vacancy_anchor = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        vacancy_name = vacancy_anchor.getText()
        vacancy_info['name'] = vacancy_name

        vacancy_link = vacancy_anchor['href']
        vacancy_info['link'] = vacancy_link

        vacancy_info['site'] = main_url + '/'

        vacancy_employer = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
        employer = vacancy_employer.getText()
        if employer.startswith('ООО') or employer.startswith('ТОО') or employer.startswith('АО'):
            employer = " ".join(vacancy_employer.getText().split()[:])
        else:
            employer = vacancy_employer.getText()
        vacancy_info['employer'] = employer

        vacancy_city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
        city = " ".join(vacancy_city.getText().split()[:])
        vacancy_info['city'] = city

        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if salary is None:
            min_salary = None
            max_salary = None
            currency = None
        else:
            salary = salary.getText()
            currency = salary.split()[-1]
            vacancy_info['currency'] = currency

            if salary.startswith('до'):
                max_salary = int("".join([s for s in salary.split() if s.isdigit()]))
                min_salary = None

            elif salary.startswith('от'):
                max_salary = None
                min_salary = int("".join([s for s in salary.split() if s.isdigit()]))

            else:
                max_salary = int("".join([s for s in salary.split('–')[1] if s.isdigit()]))
                min_salary = int("".join([s for s in salary.split('–')[0] if s.isdigit()]))

            vacancy_info['min_salary'] = min_salary
            vacancy_info['max_salary'] = max_salary

        vacancy_hh.replace_one({"link": vacancy_link}, vacancy_info, upsert=True)

    params['page'] = params['page'] + 1


# vacancy_hh.drop()

a = vacancy_hh.count_documents({})
print(a)

# for vacancy in vacancy_hh.find():
#     pprint(vacancy)

