from datetime import datetime
import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

news_list = []

def lenta_news():

    url = 'https://lenta.ru/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

    response = requests.get(url, headers=headers)

    dom = html.fromstring(response.text)
    news = dom.xpath("//a[@class='card-mini _compact']")

    for item in news:
        news_info = {}

        source_name = url
        news_title = item.xpath(".//div[@class='card-mini__text']//text()")
        news_url = url + item.xpath(".//@href")[0]

        news_response = requests.get(news_url, headers=headers)
        news_dom = html.fromstring(news_response.text)
        publication_date = news_dom.xpath("//time[@class='topic-header__item topic-header__time']//text()")[0].split(',')[1]

        news_info['source_name'] = source_name
        news_info['news_title'] = news_title
        news_info['news_url'] = news_url
        news_info['publication_date'] = publication_date

        news_list.append(news_info)

    return news_list


def mail_news():

    url = 'https://news.mail.ru/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    # Для новостей с фото:
    links = dom.xpath("//div[contains(@class, 'daynews__item')]")

    for link in links:
        news_info = {}

        news_url = link.xpath('.//@href')[0]

        news_response = requests.get(news_url, headers=headers)
        news_dom = html.fromstring(news_response.text)

        source_name = news_dom.xpath("//span[@class='note']//span[@class='link__text']/text()")
        news_title = news_dom.xpath(".//h1/text()")
        publication_date = datetime.today().strftime('%d %B %Y')

        news_info['source_name'] = source_name
        news_info['news_title'] = news_title
        news_info['news_url'] = news_url
        news_info['publication_date'] = publication_date

        news_list.append(news_info)

    # Для новостей текстом:
    links_text = dom.xpath("//ul[contains(@class, 'list_half')]/li[@class='list__item']")

    for link in links_text:
        news_info = {}

        news_url = link.xpath('.//@href')[0]

        news_response = requests.get(news_url, headers=headers)
        news_dom = html.fromstring(news_response.text)

        source_name = news_dom.xpath("//span[@class='note']//span[@class='link__text']/text()")
        news_title = news_dom.xpath(".//h1/text()")
        publication_date = datetime.today().strftime('%d %B %Y')

        news_info['source_name'] = source_name
        news_info['news_title'] = news_title
        news_info['news_url'] = news_url
        news_info['publication_date'] = publication_date

        news_list.append(news_info)

    return news_list


def yandex_news():
    
    url = 'https://yandex.ru/news/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

    response = requests.get(url, headers=headers)

    dom = html.fromstring(response.text)
    news = dom.xpath("//div[contains(@class, 'news-top-flexible-stories')]/div[contains(@class, 'mg-grid__col')]")

    for item in news:
        news_info = {}

        source_name = item.xpath("..//span[@class='mg-card-source__source']//text()")
        news_title = item.xpath(".//h2/a/text()")
        news_url = item.xpath(".//h2/a/@href")
        publication_date = datetime.today().strftime('%d %B %Y')

        news_info['source_name'] = source_name
        news_info['news_title'] = news_title
        news_info['news_url'] = news_url
        news_info['publication_date'] = publication_date

        news_list.append(news_info)

    return news_list

lenta_news()
mail_news()
yandex_news()

client = MongoClient('127.0.0.1', 27017)
db = client['news']
news = db.news
# news.insert_many(news_list)

# for item in news.find():
#     pprint(item)