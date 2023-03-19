import openai, core

from settings import openai_api_key
from datetime import datetime


class ChatGPT:
	def __init__(self, user_id: int):
		openai.api_key = openai_api_key
		self.db = core.Database(base_name="AI")
		
		self.user_id = str(user_id)
		self.messages = self.db.get(self.user_id)
		if not self.messages: # if user_id isn't in database
			self.db.set(self.user_id, [None])
			self.messages = [None]
		
		self.conversation_limit = 5
		self.user_limit_status = f"{len(self.messages)}/{self.conversation_limit}"
	
	def prompt(self, message: str):
		self.messages = self.db.get(self.user_id)
		
		if len(self.messages) > self.conversation_limit:
			self.db.set(self.user_id, [None])
			self.messages = [None]
		
		# update current date and time
		self.messages[0] = {"role": "system", "content": f"Сегодня {datetime.utcnow()} по UTC+0. Если пользователь спросит время и/или дату без указания часового пояса скажи время по UTC+0."}
		self.messages.append(
			{"role": "user", "content": message}
		)
		
		# update database
		self.db.set(self.user_id, self.messages)
		
		completion = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=self.messages
		)
		
		return completion.choices[0].message.content