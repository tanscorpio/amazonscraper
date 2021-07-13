# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Text
from itemadapter import ItemAdapter
import sqlite3


class MyproPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()
        
    def create_connection(self):
        self.conn=sqlite3.connect("mytable.db")
        self.curr=self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS mytable""")
        self.curr.execute(""" create table mytable(
                    Product Name text,
                    Price text,
                    Image Link text) """ )
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""insert into  mytable values (?,?,?)""",(
                    str(item['product_name']),
                    str(item['product_price']),
                    str(item['product_img']),)  )
        self.conn.commit()