import discord

from discord.ext.commands import Cog
from discord.ext.bridge import bridge_command, bridge_option

from common.formatters import make_embed, reply

class Utility(
	Cog,
	name="utility"
):
	def __init__(self, bot):
		self.bot = bot
	
	@bridge_command()
	@bridge_option("member", discord.Member, required=False)
	async def avatar(self, ctx, member: discord.Member):
		avatar_url = ctx.author.avatar.url if not member else member.avatar.url
		
		embed = make_embed(
			ctx,
			image=dict(url=avatar_url)
		)
		
		await reply(ctx, embed=embed)

def setup(bot):
	bot.add_cog(Utility(bot))