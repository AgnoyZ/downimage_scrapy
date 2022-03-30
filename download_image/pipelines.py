# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline  # 提供了数据下载功能
# from scrapy.pipelines.media import MediaPipeline  # 提供下载视频功能
import scrapy
 
 
class imgsPipeline(ImagesPipeline):  # 继承ImagesPipeline
 
    # 更据图片地址进行请求发送
    def get_media_requests(self, item, info):
        # 更据图片地址发起请求
        yield scrapy.Request(item["url"], meta={"item": item})
 
    # 返回图片名称即可
    def file_path(self, request, response=None, info=None, *, item=None):
        # 通过request获取meta
        item = request.meta['item']
        print('########',item)
        filePath = item['filename']
        return filePath  # 只需要返回图片的名字
 
    # 将item传递给下一个即将被执行的管道类
    def item_completed(self, results, item, info):
        return item