import scrapy
from books.items import BooksItem


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    #where to start scraping
    start_urls = ["https://books.toscrape.com/"] 

    #how to parse the response
    def parse(self, response):
        for book in response.css("article.product_pod"):
            item = BooksItem()
            item["url"] = book.css("h3 > a::attr(href)").get()
            item["title"] = book.css("h3 > a::attr(title)").get()
            item["price"] = book.css(".price_color::text").get()
            yield item
        
        #handle pagination
        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)