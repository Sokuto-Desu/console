import settings
from utils import make_embed, reply

from discord.ext.bridge import bridge_group
from discord.ext.commands import Cog


class Info(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	
	@bridge_group(description="info about something")
	async def info(self, ctx):
		pass
	
	@info.command(
		description="full info about /echo command",
		usage=f"os.info echo"
	)
	async def echo(self, ctx):
		embed = make_embed(
			ctx,
			title="/echo command info.",
			description=settings.echo_info
		)
		
		await reply(ctx, embed=embed)


def setup(bot):
	bot.add_cog(Info(bot))
