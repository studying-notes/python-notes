'''
Date: 2021-04-01 19:12:08
LastEditors: Rustle Karl
LastEditTime: 2021-04-06 07:27:21
'''
from pymongo import MongoClient
from bson.objectid import ObjectId
from hashlib import blake2b

client = MongoClient()
girls = client['girls']

cute_gils = girls.cute

cute_gils.drop()

_id = ObjectId(blake2b('string'.encode('utf-8'), digest_size=12).hexdigest())

_item = cute_gils.find_one({'_id': _id})
_item is None

cute_gils.insert_one(
    {
        '_id': _id,
        'age': 18,
        'image': [1, 2, 3]
    }
)

item = {
    'age': 18,
    'image': [1, 2, 3, 4, 5, 6]
}

_item['image'] = _item['image']+item['image'][len(_item):]
del _item['_id']
cute_gils.update_one({'_id': _id}, {'$set': _item})
