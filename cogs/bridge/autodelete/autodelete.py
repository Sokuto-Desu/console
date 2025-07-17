import discord

from discord.ext.commands import Cog
from discord.ext.bridge import bridge_command, bridge_group

from common.formatters import make_embed, reply

class Autodelete(
	Cog,
	name="autodelete"
):
	def __init__(self, bot):
		self.bot = bot
	
	@bridge_group()
	async def autodelete(self, ctx):
		pass
	
	@autodelete.command()
	async def add(self, ctx):
		pass

def setup(bot):
	bot.add_cog(Autodelete(bot))