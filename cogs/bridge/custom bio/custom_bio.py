import discord

from discord import Embed
from discord.ext.bridge import bridge_command
from discord.ext.commands import Cog

from utils import make_embed, reply
from db import DetaBase
from .assets import BioView

class CustomBioEmbed(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = DetaBase("bio")
	
	
	@bridge_command(
		name="bio",
		description="edit your custom embed that'll only belong to you!",
		usage="os.bio",
		brief="os.bio"
	)
	async def bio(self, ctx, member: discord.Member=None):
		if not member:
			member = ctx.author
			view = BioView()
		else:
			view = None
			if member.bot:
				return await reply(ctx, "Bots ain't got a personal bio bro")
		
		if user_bio := self.db.get(str(member.id)):
			embed = Embed.from_dict(user_bio)
		else:
			embed = make_embed(
				ctx, 
				title="Current personal embed is empty.",
				no_default_footer=True 
			)
		
		await reply(ctx, embed=embed, view=view)


def setup(bot):
	bot.add_cog(CustomBioEmbed(bot))