import discord
import settings

from utils import reply, DetaBase
from settings import get_guild_prefix

from discord.ext.commands import Cog
from discord.ext.bridge import bridge_group
from discord import option

class Prefix(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = DetaBase("prefixes")
	
	
	@bridge_group()
	async def prefix(self, ctx):
		if not ctx.invoked_subcommand:
			current_prefix = ctx.prefix
			await reply(ctx, f"""`my current prefix is "{current_prefix}".\nuse "{current_prefix}prefix set >new_prefix" to set new prefix.`""")
	
	
	@prefix.command(
		name="set",
		description="set new bot's prefix for this server",
		usage="os.prefix set >new_prefix",
		brief="os.prefix set cmd. // os.prefix set $"
	)
	@option("prefix", description="new prefix", required=True)
	async def _set(self, ctx, prefix: str=None):
		if not prefix:
			return await reply(ctx, "`please properly provide the prefix.`")
		
		guild_id = str(ctx.guild.id)
		self.db.set(key=guild_id, value=prefix)
		
		await reply(ctx, f"""`successfully set "{prefix}" as new prefix.`""")
	
	@prefix.command(
		name="reset",
		description="reset bot's prefix for this server",
		usage="os.prefix reset",
		brief=""
	)
	async def _reset(self, ctx):
		guild_id = str(ctx.guild.id)
		self.db.delete(guild_id)
		
		await reply(ctx, "`successfully reset bot's prefix.`")
	
	


def setup(bot):
	bot.add_cog(Prefix(bot))