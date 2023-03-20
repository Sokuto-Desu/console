from settings import deta_key
from deta import Deta


class Database:
	def __init__(self, base_name):
		self.collection = Deta(deta_key)
		self.base = self.collection.Base(base_name)
	
	
	def set(self, key: str, value):
		return self.base.put(key=key, data=value)
	
	def get(self, key: str):
		item = self.base.get(key=key)
		if item:
			return item["value"]
		else:
			return None
	
	def delete(self, key: str):
		self.base.delete(key=key) # deta delete method always returns None so
		return True # here it returns True