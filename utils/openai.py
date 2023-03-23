import openai, functools

from settings import openai_api_key
from datetime import datetime
from asyncio import get_running_loop
from .db import Database


class GPT:
	def __init__(self, user_id: int, system_message: str=None):
		openai.api_key = openai_api_key
		self.db = Database(base_name="AI")
		
		self.user_id = str(user_id)
		self.messages = self.db.get(self.user_id, default=[None])
		
		self.conversation_limit = self.db.get("limit", default=5)
		self.user_limit_status = self.count_user_messages()
		
		self.default_system_message = (
			f"Today is {datetime.utcnow()} by UTC. "
			"You are GPT-3.5. Answer as concisely as possible. "
			"All the information provided is available to you in any languages. "
		)
		self.system_message = system_message or self.db.get("system_message", default=self.default_system_message)
	
	
	async def count_user_messages(self) -> int:
		user_messages_amount = 1
		
		for message in self.messages:
			if message.get("role") == "user":
				user_messages_amount += 1
		
		return f"{user_messages_amount}/{self.conversation_limit}"
	
	async def update_limit_status(self) -> None:
		user_messages_amount = self.count_user_messages()
		
		if user_messages_amount > self.conversation_limit: # reset conversation when limit reached
			return await self.erase_dialogue()
		
		self.user_limit_status = user_messages_amount
	
	
	async def update_info(self):
		self.messages = self.db.get(self.user_id, default=[None])
		await self.update_limit_status()
	
	async def erase_dialogue(self):
		self.messages = [None]
		self.db.set(self.user_id, [None])
	
	
	async def prompt(self, prompt_message: str, ai_model: str="gpt-3.5-turbo") -> str:
		await self.update_info()
		
		self.messages[0] = {"role": "system", "content": self.system_message}
		self.messages.append({"role": "user", "content": prompt_message})
		
		try:
			loop = get_running_loop()
			response = await loop.run_in_executor( # turning sync to async
				None,
				functools.partial( # creates a new function that calls create() with kwargs. run_in_executor doesn't have kwargs so i used this
					openai.ChatCompletion.create,
					model=ai_model,
					messages=self.messages
				)
			)
		except openai.error.RateLimitError:
			return "I am currently overloaded with requests. Try again later."
		
		assistant_message = response.choices[0].message
		self.messages.append(assistant_message)
		self.db.set(self.user_id, self.messages)
		
		return assistant_message.content