import sys

from settings import devserver
from asyncio import get_running_loop
from utils import reply

from discord import option
from discord.ext.commands import Cog
from discord.ext.bridge import bridge_command


class Owner(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	
	async def cog_check(self, ctx):
		return await self.bot.is_owner(ctx.author)
	
	
	@bridge_command(hidden=True, guild_ids=[devserver])
	@option("mode", required=True, choices=["eval", "exec"])
	@option("data", required=True)
	async def run(self, ctx, mode: str, *, data: str):
		if mode == "eval":
			try:
				result = eval(data)
			except SyntaxError:
				result = await eval(data)
			
			await reply(ctx, f"```py\n{result}```")
		
		elif mode == "exec":
			# insert two tabs to every line except first
			tabed_code = "\n\t\t".join(data.split("\n"))
			
			globals_ = globals().update({"self": self, "bot": self.bot, "ctx": ctx})
			
			return exec(
			f"""
async def __ex():
	try:
		{tabed_code}
	except Exception as e:
		await ctx.respond(str(e)[:1995])
get_running_loop().create_task(__ex())""",
			globals_)
	
	
	@bridge_command(aliases=["sd"], hidden=True, guild_ids=[devserver])
	async def shutdown(self, ctx):
		await reply(ctx, "`closing connection...`")
		await self.bot.close()
		sys.quit()


def setup(bot):
	bot.add_cog(Owner(bot))