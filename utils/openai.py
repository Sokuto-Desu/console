import openai, core, functools

from settings import openai_api_key
from datetime import datetime
from asyncio import get_running_loop


class ChatGPT:
	def __init__(self, user_id: int):
		openai.api_key = openai_api_key
		self.db = core.Database(base_name="AI")
		
		self.user_id = str(user_id)
		self.messages = self.db.get(self.user_id)
		if not self.messages: # if user_id isn't in database
			self.db.set(self.user_id, [None])
			self.messages = [None]
		
		self.conversation_limit = 10
		self.user_limit_status = f"{self.count_user_messages()}/{self.conversation_limit}"
	
	
	def count_user_messages(self):
		user_messages = 1
		for message in self.messages:
			if not message:
				return 1
			if message.get("role") == "user":
				user_messages += 1
		return user_messages
	
	async def prompt(self, message: str):
		self.messages = self.db.get(self.user_id)
		
		if self.count_user_messages() > self.conversation_limit: # reset conversation when limit reached
			self.db.set(self.user_id, [None])
			self.messages = [None]
		
		# update limit status
		self.user_limit_status = f"{self.count_user_messages()}/{self.conversation_limit}"
		
		self.messages[0] = {"role": "system", "content": f"Сегодня {datetime.utcnow()} по UTC+0.\nТы — ChatGPT, большая языковая модель, обученная OpenAI. Отвечай как можно лаконичнее. Если пользователь скажет как тебе вести себя, всегда веди себя так, как сказал пользователь. \nОграничение знаний: 2021-09-01\nВся эта информация доступна тебе в любых языках."}
		self.messages.append(
			{"role": "user", "content": message}
		)
		self.db.set(self.user_id, self.messages)
		
		try:
			loop = get_running_loop()
			completion = await loop.run_in_executor( # turning sync to async
				None,
				functools.partial( # creates a new function that calls create() with kwargs. run_in_executor doesn't have kwargs so i used partial()
					openai.ChatCompletion.create,
					model="gpt-3.5-turbo",
					messages=self.messages
				)
			)
		except openai.error.RateLimitError:
			self.messages.pop(-1) # delete last prompt
			self.db.set(self.user_id, self.messages)
			return "I am currently overloaded with requests. Try later."
		
		result_message = completion.choices[0].message
		self.messages.append(result_message) # "assistant" role message
		self.db.set(self.user_id, self.messages)
		
		return result_message.content
	
	async def erase_dialogue(self):
		self.db.set(self.user_id, [None])
		self.messages = [None]