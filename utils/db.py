from deta import Deta
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class Database:
	def __init__(self, base_name):
		deta_key = getenv("DETA_KEY")
		self.collection = Deta(deta_key)
		self.base = self.collection.Base(base_name)
	
	
	def set(self, key: str, value):
		return self.base.put(key=key, data=value)["value"]
	
	def get(self, key: str, set_default=None):
		if item := self.base.get(key=key):
			return item["value"]
		else:
			return self.set(key=key, value=set_default)
	
	def delete(self, key: str):
		self.base.delete(key=key) # deta delete method always returns None so
		return True # here it returns True