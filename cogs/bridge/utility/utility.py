import discord

from discord.ext.commands import Cog
from discord.ext.bridge import bridge_command

from core.formatters import make_embed

class Utility(
	Cog,
	name="utility"
):
	def __init__(self, bot):
		self.bot = bot
	
	@bridge_command()
	async def avatar(self, ctx, member: discord.Member=None):
		avatar_url = ctx.author.avatar.url if not member else member.avatar.url
		
		embed = make_embed(
			ctx,
			image=dict(url=avatar_url)
		)
		
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Utility(bot))