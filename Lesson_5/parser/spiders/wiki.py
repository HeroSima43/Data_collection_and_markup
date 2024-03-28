import scrapy


class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Index_of_Economic_Freedom"]

    # def parse(self, response):
    #     pass

    def parse(self, response):
        countries = response.xpath("//tbody/tr")
        for country in countries:
            name = country.xpath(".//td[1]/a/text()").get()
            rank = country.xpath(".//td[2]/text()").get()
            score = country.xpath(".//td[3]/text()").get()
            yield {
                'country_name': name,
                'Rank': rank,
                'Score': score,
            }