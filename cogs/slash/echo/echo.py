import discord

from discord.ext.commands import Cog
from discord import slash_command

class Echo(
	Cog,
	name="echo"
):
	def __init__(self, bot):
		self.bot = bot 
	
	@slash_command(
		name="echo"
	)
	async def echo(
		self,
		ctx,
		content: str
	):
		await ctx.respond(content)

def setup(bot):
	bot.add_cog(Echo(bot))