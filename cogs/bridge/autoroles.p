from core import Database

from discord import slash_command, default_permissions
from discord.ext.commands import Cog


class Autoroles(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = Database()
	
	@slash_command()
	&default_permissions(manage_roles)
	async def 