import discord
from discord import slash_command
from discord.ext import commands
from discord.commands import Option

from settings import config


class Owner(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_check(self, ctx):
		return self.bot.is_owner(ctx.author)
	
	
	@slash_command(guild_ids = config["devserver"])
	async def run(self, ctx, c: Option(str, required = True, choices = ["eval", "exec"]), *, data: Option(str, required = True)):
		if c = "eval:
			try:
				r = eval(data)
			except:
				r = await eval(data)
			
			await ctx.respond(f"```py\n{r}```")
		
		elif c == "exec:
			data = "\n" + data if not data.startswith("\n") else data
			tabed_code = "  ".join(data.split("\n")).replace("  ", "\n  ")
			
			clcb = asyncio.get_running_loop()
			
			return exec(f"async def __ex():\n	try:\n{tabed_code}\n	except Exception as e:\n		await ctx.respond(str(e)[0:1995])\nclcb.create_task(__ex())", globals().update({"bot": bot, "ctx": ctx}))
	
	
	@slash_command(guild_ids = config["devserver"])
	async def shutdown(self, ctx):
		await ctx.respond("`closing connection...`")
		await bot.close()


def setup(bot):
	bot.add_cog(Owner(bot))