import settings

import discord
from discord import slash_command
from discord.ext import commands
from discord.commands import Option


class Owner(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_check(self, ctx):
		return self.bot.is_owner(ctx.author)
	
	
	@slash_command(guild_ids = settings.devserver)
	@option("mode", required = True, choices = ["eval", "exec"])
	@option("data", required = True)
	async def run(self, ctx, mode: str, *, data: str):
		if mode == "eval":
			try:
				r = eval(data)
			except:
				r = await eval(data)
			
			await ctx.respond(f"```py\n{r}```")
		
		elif mode == "exec":
			data = "\n" + data if not data.startswith("\n") else data
			tabed_code = "  ".join(data.split("\n")).replace("  ", "\n  ")
			
			_running_loop = asyncio.get_running_loop()
			
			return exec(f"async def __ex():\n	try:\n{tabed_code}\n	except Exception as e:\n		await ctx.respond(str(e)[0:1995])\n_running_loop.create_task(__ex())", globals().update({"bot": bot, "ctx": ctx}))
	
	
	@slash_command(guild_ids = settings.devserver)
	async def shutdown(self, ctx):
		await ctx.respond("`closing connection...`")
		await bot.close()


def setup(bot):
	bot.add_cog(Owner(bot))