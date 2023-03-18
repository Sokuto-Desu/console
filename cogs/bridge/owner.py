import random, openai

from settings import devserver
from asyncio import get_running_loop, sleep
from utils import reply
from core import Database

from discord import option
from discord.ext.commands import Cog, command, is_owner
from discord.ext.bridge import bridge_command

openai.api_key = "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"

class Owner(Cog):
	def __init__(self, bot):
		self.bot = bot
#		self.owner_id = 898610134589243442
	
	
#	async def cog_check(self, ctx):
#		return self.owner_id == ctx.author.id
	
	
	@bridge_command(hidden=True, guild_ids=[devserver])
	@is_owner()
	@option("mode", required=True, choices=["eval", "exec"])
	@option("data", required=True)
	async def run(self, ctx, mode: str, *, data: str):
		if mode == "eval":
			try:
				result = eval(data)
			except SyntaxError:
				result = await eval(data)
			
			await ctx.respond(f"```py\n{result}```")
		
		elif mode == "exec":
			# insert two tabs to every line except first
			tabed_code = "\n\t\t".join(data.split("\n"))
			
			_running_loop = get_running_loop()
			
			return exec(f"""
async def __ex():
	try:
		{tabed_code}
	except Exception as e:
		await ctx.respond(str(e)[:1995])
_running_loop.create_task(__ex())""", globals().update({"self": self, "bot": self.bot, "ctx": ctx}))
	
	
	@bridge_command(aliases=["sd"], hidden=True, guild_ids=[devserver])
	@is_owner()
	async def shutdown(self, ctx):
		await reply(ctx, "`closing connection...`")
		await self.bot.close()
	
	async def say_random(self, ctx):
		sentences = Database().get("AI")
		sentence = random.choice(sentences).split()
		
		for index, x in enumerate(sentence):
			if random.randint(0, 1):
				try:
					sentence[index] = random.choice(random.choice(sentences).split())
				except IndexError:
					pass
		
		reply = " ".join(sentence)
		await ctx.send(reply)
	
	@command()
	async def chat(self, ctx, *, prompt):
		message = await ctx.send("`please wait a minute.`")
		
		result = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
		
		await message.edit(f"`please wait a minute.`\n```\n{result.choices[0].message.content}```")


def setup(bot):
	bot.add_cog(Owner(bot))