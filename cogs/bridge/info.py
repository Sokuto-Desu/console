import settings
from utils import make_embed

from discord.ext.bridge import bridge_group
from discord.ext.commands import Cog


class Info(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	
	@bridge_group()
	async def info(self, ctx):
		pass
	
	@info.command(
		description="echo info",
		usage=f"os.info echo"
	)
	async def echo(self, ctx):
		embed = make_embed(
			title="/echo command info.",
			description=settings.echo_info
		)
		
		await ctx.respond(embed=embed)


def setup(bot):
	bot.add_cog(Info(bot))
