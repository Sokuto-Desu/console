from settings import deta_key
from deta import Deta


class Collection:
	def __init__(self):
		self.__deta_collection = Deta(deta_key)
	
	def get_base(self, base_name: str):
		return self.__deta_collection.Base(base_name)

class Database(Collection):
	def __init__(self, base_name="ConsoleDB"): # do NOT provide base_name if its not necessary.
		self.base = get_base(base_name)
	
	
	def set(self, key: str, value):
		return self.base.put(key=key, data=value)
	
	def get(self, key: str):
		return self.base.get(key=key)
	
	def delete(self, key: str):
		self.base.delete(key=key) # deta delete method always returns None so
		return True # here it returns True