from discord.ext.commands import Cog
from discord.ext.bridge import bridge_command, bridge_option

from common import config, formatters

from . import execution

class Developer(
	Cog,
	name="developer",
	command_attrs=dict(
		hidden=True,
		guild_ids=[config.developer_server])
):
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_check(self, ctx):
		return await self.bot.is_owner(ctx.author)
	
	@bridge_command(aliases=["code"])
	@bridge_option("mode", required=True, choices=["eval", "exec"])
	@bridge_option("data", required=True)
	async def run(self, ctx, mode: str, *, data: str):
		if mode == "eval":
			result = await execution.evaluate(data)
			await formatters.reply(ctx, f"```py\n{result}```")
		else:
			await execution.execute(data, self, self.bot, ctx)
	
	
	@bridge_command(aliases=["sd"])
	async def shutdown(self, ctx):
		await formatters.reply(ctx, "`closing connection...`")
		await self.bot.close()


def setup(bot):
	bot.add_cog(Developer(bot))
