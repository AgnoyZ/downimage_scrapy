import scrapy
import re
import requests
from scrapy.http import HtmlResponse
from scrapy import Selector
from download_image.items import DownloadImageItem
from scrapy.utils.project import get_project_settings


class WallpaperSpider(scrapy.Spider):
    name = 'wallpaper'
    allowed_domains = ['wallhaven.cc']
    def start_requests(self):
        url_list = []
        pattern = re.compile(r'><a class="preview" href="https://wallhaven.cc/w/.{6}"')
        settings = get_project_settings()
        for page in range(1, settings.get('MAX_PAGE')+1):
            site = f'https://wallhaven.cc/toplist?page={page}'
            with requests.get(site) as resp:
                if resp.status_code == 200:
                    url_list.extend(pattern.findall(resp.text))
        length = len(url_list)
        for i in range(length):
            url_list[i] = url_list[i][26:-1]
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: HtmlResponse):
        sel = Selector(response)
        image_item = sel.re(r'https://w.wallhaven.cc/full/.{2}/wallhaven-.{6}..{3}')
        for sel_image in image_item:
            item = DownloadImageItem()
            item['filename'] = sel_image[sel_image.rfind('/') + 1:]
            item['url'] = sel_image
            yield item
