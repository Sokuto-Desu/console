from settings import deta_key
from deta import Deta


class Database:
	def __init__(self, base_name="ConsoleDB"): # do NOT provide base_name if its not necessary.
		self.collection = Deta(deta_key)
		self.base = self.collection.Base(base_name)
	
	
	def set(self, key: str, value):
		return self.base.put(key=key, data=value)
	
	def get(self, key: str):
		return self.base.get(key=key)["value"]
	
	def delete(self, key: str):
		self.base.delete(key=key) # deta delete method always returns None so
		return True # here it returns True