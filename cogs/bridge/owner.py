from settings import devserver
from utils import reply, get_traceback

from discord import option
from discord.ext.commands import Cog
from discord.ext.bridge import bridge_command


class Owner(
	Cog,
	command_attrs=dict(
		hidden=True,
		guild_ids=[devserver])
	):
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_check(self, ctx):
		return await self.bot.is_owner(ctx.author)
	
	
	@bridge_command(aliases=["code"])
	@option("mode", required=True, choices=["eval", "exec"])
	@option("data", required=True)
	async def run(self, ctx, mode: str, *, data: str):
		if mode == "eval":
			try:
				result = eval(data)
			except SyntaxError:
				result = await eval(data)
			except Exception as e:
				result = f"```\n{get_traceback(e)}```"
			
			await reply(ctx, f"```py\n{result}```")
		
		else:
			tabbed_code = "\n\t\t".join(data.split("\n")) # splits data by lines and tabs them (so execute() will work)
			formatted_code = tabbed_code.replace("dprint", "await ctx.send") # for convenience ¯\_(ツ)_/¯
			
			_globals = globals().update(
				{
					"self": self,
					"bot": self.bot,
					"ctx": ctx,
					"formatted_code": formatted_code
				}
			)
			
			exec(
				"async def execute():"
				"\n\ttry:"
				f"\n\t\t{formatted_code}" # tab at the beginning cause tabbed_code tabbed every line except first
				"\n\texcept Exception as e:"
				"\n\t\tawait reply(ctx, get_traceback(e))"
				"\nbot.loop.create_task(execute())",
				_globals,
				locals()
			)
	
	
	@bridge_command(aliases=["sd"])
	async def shutdown(self, ctx):
		await reply(ctx, "`closing connection...`")
		await self.bot.close()


def setup(bot):
	bot.add_cog(Owner(bot))