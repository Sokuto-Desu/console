import rapidjson as json

from deta import Deta
from dotenv import load_dotenv
from os import getenv, getcwd, path

load_dotenv()


class DetaBase:
	def __init__(self, base_name):
		deta_key = getenv("DETA_KEY")
		self.collection = Deta(deta_key)
		self.base_name = base_name
		self.base = self.collection.Base(base_name)
		# idfk why but open() refuses to work if i dont set full path to this file like THIS
		self.cache_path = f"{getcwd()}{path.sep}db{path.sep}cache.json" 
	
	
	def add_to_cache(self, key: str, value):
		"Adds an element to cache (json file)"
		with open(self.cache_path) as f:
			# for deta base separation
			cache_key = f"{self.base_name} {key}" 
			cache_dict = json.load(f)
			cache_dict[cache_key] = value 
		
		with open(self.cache_path, "w") as f:
			json.dump(cache_dict, f, skipkeys=True)
	
	def get_from_cache(self, key: str):
		"Gets a value from cache (json file)"
		with open(self.cache_path) as f:
			cache_key = f"{self.base_name} {key}"
			# .get() is a dict call
			if cached_value := json.load(f).get(cache_key): 
				return cached_value
	
	def delete_from_cache(self, key: str):
		"Removes an element from cache (json file)"
		with open(self.cache_path) as f:
			cache_key = f"{self.base_name} {key}"
			cache_dict = json.load(f)
			try:
				cache_dict.pop(cache_key)
			except KeyError:
				pass
		
		with open(self.cache_path, "w") as f:
			json.dump(cache_dict, f, skipkeys=True)
	
	
	def set(self, key: str, value):
		"Sets a value in Deta Base and adds it to cache (json file), then returns the set value."
		if not isinstance(value, dict):
			return_value = self.base.put(key=key, data=value).get("value")
		else:
			# Deta for some reason makes dictionaries a part of item and doesn't set it to item's "value"
			corrected_value = {"value": value}
			return_value = self.base.put(key=key, data=corrected_value)
		
		self.add_to_cache(key, value)
		
		return return_value
	
	def get(self, key: str, set_default=None):
		"""
		Checks if a value is in cache (json file) and returns it.
		On fail, sets the value to set_default if provided, and returns the value from Deta Base.
		You always should use this and not _get(), unless you for some reason don't need caching and set_default at all.
		"""
		if cached_value := self.get_from_cache(key):
			return cached_value
		
		value = self._get(key=key)
		
		if value and not set_default:
			return value
		else:
			return self.set(key=key, value=set_default)
	
	def _get(self, key: str):
		"Checks if a value in Deta Base exists and returns it, else returns None."
		if item := self.base.get(key=key): # if exists
			return item.get("value")
		else:
			return None
	
	def delete(self, key: str):
		"Deletes a value from Deta Base and cache (json file), then returns True."
		self.base.delete(key=key)
		self.delete_from_cache(key)
		
		# deta's delete method always returns None so here it returns True
		return True 