import re
import uuid

import request as request
import requests
from bs4 import BeautifulSoup

from src.common.database import Database
from src.models.items import constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self,name,url,price=None,_id = None):
        self.name = name
        self.url =url
        store = Store.find_by_url(url)
        self._id = uuid.uuid4().hex if _id is None else _id
        self.tag_name = store.tag_name
        self.query = store.query
        print(store)
        self.price = None if price is None else price

    def __repr__(self):
        return "<Item {} with url {}>".format(self.name,self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content,"html.parser")
        print(self.tag_name, self.query)
        element = soup.find(self.tag_name , self.query)
        string_price=element.text.strip()
        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price =float(match.group())
        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION,{ "_id":self._id },self.json())

    def json(self):
        return {
            "name":self.name,
            "url":self.url,
            "_id":self._id,
             "price":self.price
             }
    @classmethod
    def get_by_id(cls,id):
        return cls(**Database.find_one(ItemConstants.COLLECTION,{"_id":id}))