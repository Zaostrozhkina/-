# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

class CastoramaparserPipeline:
    def process_item(self, item, spider):
        if spider.name == 'castorama':
            item["spec"] = {}
            n = 0
            for i in item["spec_name"]:
                try:
                    item["spec"][i] = item["spec_value"][n]
                    n += 1
                except:
                    IndexError
        return item


class CastoramaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = item['name']
        number_of_photo = request.url.split('.')[-2][-1]
        image_filename = f'{image_name}/#{number_of_photo}.jpg'
        return image_filename

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item