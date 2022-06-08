import scrapy
from scrapy.http import HtmlResponse
from castoramaparser.items import CastoramaparserItem
from scrapy.loader import ItemLoader

class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='pages']//li/a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-card__img-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaparserItem(), response=response)
        loader.add_value("link", response.url)
        loader.add_xpath("name", "//h1[@itemprop='name']/text()")
        loader.add_xpath("price", "//span[@class='price']/span/span/text()")
        loader.add_xpath("currency", "//span[@class='price']//span[@class='currency']/text()")
        loader.add_xpath("photos", "//span[@itemprop='image']/@content")
        loader.add_xpath("spec_name", "//dl[contains(@class, 'specs-table')]/dt[contains(@class, 'specs-table__attribute-label')]/span/text()")
        loader.add_xpath("spec_value", "//dl[contains(@class, 'specs-table')]/dd[contains(@class, 'specs-table__attribute-value ')]/text()")
        yield loader.load_item()


# //li//img[contains(@class, 'top-slide__img')]/@src
# //span[@itemprop='image']/@content
