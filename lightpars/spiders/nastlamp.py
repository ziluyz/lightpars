import scrapy
import csv

class NastlampSpider(scrapy.Spider):
    name = "nastlamp"
    allowed_domains = ["intersvetneo.ru"]
    start_urls = ["https://intersvetneo.ru/catalog/nastolnye-lampy/dekorativnye/"]

    def parse(self, response):
        file = open('nastlamp.csv', 'a')
        writer = csv.DictWriter(file, fieldnames=['name', 'url', 'price'])
        for product in response.css("div.item_info.TYPE_1"):
            record = {
                "name": product.css("div.item-title a span::text").get(),
                "url": product.css("div.item-title a::attr(href)").get(),
                "price": product.css("div.price::attr(data-value)").get() + " " + product.css("div.price::attr(data-currency)").get()
            }
            writer.writerow(record)
            yield record

        file.close()
        next_page = response.css("a.flex-next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
