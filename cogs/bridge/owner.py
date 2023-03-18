import random

from settings import devserver
from asyncio import get_running_loop, sleep
from utils import reply
from core import Database

from discord import option
from discord.ext.commands import Cog, command
from discord.ext.bridge import bridge_command


class Owner(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.owner_id = 898610134589243442
	
	
	async def cog_check(self, ctx):
		return self.owner_id == ctx.author.id
	
	
	@bridge_command(hidden=True, guild_ids=[devserver])
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
	async def shutdown(self, ctx):
		await reply(ctx, "`closing connection...`")
		await self.bot.close()


def setup(bot):
	bot.add_cog(Owner(bot))