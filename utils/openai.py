import openai, functools

from settings import openai_api_key
from datetime import datetime
from asyncio import get_running_loop
from .db import Database


class GPT:
	def __init__(self, user_id: int):
		openai.api_key = openai_api_key
		self.db = Database(base_name="AI")
		
		self.user_id = str(user_id)
		self.messages = self.db.get(self.user_id)
		if not self.messages: # if user_id isn't in database
			self.db.set(self.user_id, [None])
			self.messages = [None]
		
		self.conversation_limit = 10
		self.user_limit_status = f"{self.count_user_messages()}/{self.conversation_limit}"
	
	
	def count_user_messages(self) -> int:
		user_messages_amount = 1
		for message in self.messages:
			if not message:
				return 1
			if message.get("role") == "user":
				user_messages_amount += 1
		return user_messages_amount
	
	async def update_self(self):
		self.messages = self.db.get(self.user_id)
		
		user_messages_amount = self.count_user_messages()
		if user_messages_amount > self.conversation_limit: # reset conversation when limit reached
			await self.erase_dialogue()
		
		self.user_limit_status = f"{user_messages_amount}/{self.conversation_limit}"
	
	
	async def update_messages(self, messages: list):
		self.db.set(self.user_id, messages)
		self.messages = messages
	
	async def erase_dialogue(self):
		await self.set_messages([None])
	
	
	async def prompt(self, message: str) -> str:
		await self.update_self()
		
		self.messages[0] = {
			"role": "system",
			"content": (f"Сегодня {datetime.utcnow()} по UTC+0."
						"Ты - ChatGPT (GPT-3.5), большая языковая модель обученная OpenAI. Всегда отвечай лаконично и четко."
						"Вся эта информация доступна тебе в любых языках.")
		}
		self.messages.append({"role": "user", "content": message})
		
		try:
			loop = get_running_loop()
			completion = await loop.run_in_executor( # turning sync to async
				None,
				functools.partial( # creates a new function that calls create() with kwargs. run_in_executor doesn't have kwargs so i used this
					openai.ChatCompletion.create,
					model="gpt-3.5-turbo",
					messages=self.messages
				)
			)
		except openai.error.RateLimitError:
			return "I am currently overloaded with requests. Try later."
		
		assistant_message = completion.choices[0].message
		
		self.messages.append(assistant_message)
		await update_messages(self.messages)
		
		return assistant_message.content