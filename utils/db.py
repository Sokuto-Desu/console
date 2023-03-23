from settings import deta_key
from deta import Deta


class Database:
	def __init__(self, base_name):
		self.collection = Deta(deta_key)
		self.base = self.collection.Base(base_name)
	
	
	def set(self, key: str, to):
		return self.base.put(key=key, data=to)
	
	def get(self, key: str, default=None, set_default=None):
		if item := self.base.get(key=key):
			return item["value"]
		else:
			return self.set(key=key, to=set_default)["value"]
	
	def delete(self, key: str):
		self.base.delete(key=key) # deta delete method always returns None so
		return True # here it returns True