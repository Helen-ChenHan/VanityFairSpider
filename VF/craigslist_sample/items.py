from scrapy.item import Item, Field

class VFItem(Item):
    title = Field()
    link = Field()
    article = Field()
    date = Field()
