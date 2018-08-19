import uuid

from src.common.database import Database
from src.models.stores import constants as StoreConstants
from src.models.stores import errors as StoreErrors


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query =query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))

    def save_to_mongo(self):
        Database.insert(StoreConstants.COLLECTION, self.json())

    @classmethod
    def get_by_urlprefix(cls, url_prefix):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):

        for i in range(0,len(url)+1):
            if url[i]=="." and url[i+1]=="c" and url[i+2]=="o" and url[i+3]=="m" and url[i+4]=="/":
                count = i+4
                break

        try:
            store = cls.get_by_urlprefix(url[:count])
            return store
        except:
            raise StoreErrors.StoreNotFoundException("the store doest not exists")





    @classmethod
    def all(cls):
        return [cls(**elem)for elem in Database.find(StoreConstants.COLLECTION,{})]

    def delete(self):
        Database.delete_one(StoreConstants.COLLECTION, {'_id': self._id})

    def update_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {'_id': self._id}, self.json())
