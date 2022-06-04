import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BD%D0%B0%D1%83%D1%87%D0%BF%D0%BE%D0%BF/?stype=0']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath('//div[@class="pagination-next"]/a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow('https://www.labirint.ru' + link, callback=self.parse_books)

    def parse_books(self, response:HtmlResponse):
        link = response.url
        name = response.xpath("//meta[@property='og:title']/@content").get()
        author = response.xpath("//div[@class='authors']/a/text()").get()
        main_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        discount_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        currency = response.xpath("//span[@class='buying-pricenew-val-currency']/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()
        yield BooksparserItem(link=link, name=name, author=author, main_price=main_price,
                              discount_price=discount_price, currency=currency, rating=rating)









