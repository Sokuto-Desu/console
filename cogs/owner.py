from settings import devserver
from asyncio import get_running_loop

from discord import slash_command, option
from discord.ext.commands import Cog


class Owner(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_check(self, ctx):
		return await self.bot.is_owner(ctx.author)
	
	
	@slash_command(guild_ids=[devserver])
	@option("mode",required=True, choices=["eval", "exec"])
	@option("data", required=True)
	async def run(self, ctx, mode: str, data: str):
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
_running_loop.create_task(__ex())""", globals().update({"bot": self.bot, "ctx": ctx}))
	
	
	@slash_command(guild_ids=[devserver])
	async def shutdown(self, ctx):
		await ctx.respond("`closing connection...`")
		await self.bot.close()


def setup(bot):
	bot.add_cog(Owner(bot))