import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from ..items import UnsplashComItem
from itemloaders.processors import MapCompose
from scrapy.pipelines.images import ImagesPipeline
from pathlib import Path


class UnsplashComImgsSpider(CrawlSpider):
    name = "unsplash_com_imgs"
    allowed_domains = ["unsplash.com", "images.unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul/li/a[contains(@class, 'p7ajO') and contains(@href, '/t/')]")),
        Rule(LinkExtractor(restrict_xpaths="//figure[@itemprop='image' and @itemscope]//a[@itemprop='contentUrl' and @title]/parent::figure/a"), callback="parse_item", follow=True),
        )

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=UnsplashComItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        loader.add_xpath("description", "//div/div/h1/text()")
        loader.add_xpath("category", "//div/h3/parent::div[1]/span//a/text()")
        loader.add_xpath("author", "//div[@class='TO_TN']/a/text()")
        image_urls = response.xpath("//button/div/div/img/@src").getall()
        image_urls = [url.split("?")[0] for url in image_urls]
        loader.add_value("image_urls", image_urls)
        yield loader.load_item()
