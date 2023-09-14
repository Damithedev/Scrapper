import random

import scrapy
from bookscrapper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    user_agents_list = {
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
        'Mozilla/5.0 (Linux; Android 11; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Mobile Safari/537.36'
        'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; rv:11.0) like Gecko'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
        'Mozilla/5.0 (Linux; Android 10; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/100.0.10565.0 Safari/537.36'
    }

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url

            yield response.follow(book_url, callback=self.parse_book_page, headers={"User-Agent": self.user_agents_list[random.randint(0,len(self.user_agents_list)-1)]})

        next_page = response.css('li.next a ::attr(href)').get()
        print(next_page)
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page

            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        book_item = BookItem()

        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['product_type'] = table_rows[1].css('td::text').get(),
        book_item['price_excl_tax'] = table_rows[2].css("td::text").get(),
        book_item['price_incl_tax'] = table_rows[3].css("td::text").get(),
        book_item['tax'] = table_rows[4].css("td::text").get(),
        book_item['availability'] = table_rows[5].css("td::text").get(),
        book_item['num_reviews'] = table_rows[6].css("td::text").get(),
        book_item['stars'] = response.css('p.star-rating ::attr(class)').get(),
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] = response.css('p.price_color ::text').get(),

        yield book_item
        pass
