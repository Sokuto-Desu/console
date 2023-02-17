from core.utils import Embed
from random import choice, randint
from base64 import b64decode, b64encode

from discord.ext.commands import Cog, MemberConverter
from discord import slash_command, option


class Utility(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	
	@slash_command()
	@option("member", required=False, default=None)
	async def avatar(self, ctx, member: MemberConverter):
		member = ctx.author if member is None else member
		
		embed = Embed.create(
			title = f"`{member}'s avatar`",
			image = {"url": member.avatar.url}
		)
		await ctx.respond(embed = embed)
	
	
	@slash_command(description="random choice")
	@option("data", description="choice1, choice2, choice3 ... (random choice) | any number (random number choice)", required=True)
	async def random(self, ctx, *, data: str):
		try:
			number = int(data)
			return await ctx.respond(f"`{randint(1, number)}`")
		except ValueError:
			pass
		
		choices = [c.strip() for c in data.split(",")]
		
		await ctx.respond(f"`{choice(choices)}`")
	
	
	@slash_command(description="character to unicode / unicode to character")
	@option("get", required=True, choices=["character", "unicode"])
	@option("data", description="example: 0001 (space) | • (U+2022)", required=True)
	async def unicode(self, ctx, get: str, data: str):
		if get == "character":
			result = data.decode("utf-8")
		else:
			result = str(hex(ord(data))).replace("0x", "U+")
		
		await ctx.respond(f"`{result}`")
	
	
	@slash_command(description = "base64 encode/decode")
	@option("mode", required = True, choices = ["encode", "decode"])
	@option("data", required = True)
	async def base64(self, ctx, mode: str, data: str):
		databytes = data.encode("utf-8")
		
		if mode == "encode":
			result = b64encode(databytes)
		else:
			result = b64decode(databytes)
		
		result = result.decode("utf-8")
		
		await ctx.respond(f"`{result}`")


def setup(bot):
	bot.add_cog(Utility(bot))