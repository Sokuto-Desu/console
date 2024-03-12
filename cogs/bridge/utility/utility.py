import re
import asyncio
import random

from utils import make_embed, reply
from base64 import b64decode, b64encode

from discord.ext.commands import Cog
from discord.ext.bridge import bridge_command
from discord import option, Member


class Utility(
	Cog,
	name="Utilities",
	description="Small utilities for your server"
):
	def __init__(self, bot):
		self.bot = bot
	
	
	@bridge_command(
		description="get member avatar",
		usage="os.avatar -member", 
		brief="os.avatar <@927163003638546442>"
	)
	@option("member", required=False, default=None)
	async def avatar(self, ctx, member: Member=None):
		member = member or ctx.author
		
		embed = make_embed(
			ctx,
			title=f"`{member.name}'s avatar`",
			image=dict(
				url=member.avatar.url
			)
		)
		await ctx.respond(embed=embed)
	
	
	@bridge_command(
		aliases=["r", "rand"],
		description="random choice",
		usage="os.random >number or choices",
		brief="os.random yes, no, probably\nos.random 10"
	)
	@option("data", description="choice1, choice2, choice3 ... (random choice) | any number (random number choice)", required=True)
	async def random(self, ctx, *, data: str):
		try:
			number = int(data)
			result = f"```\n{random.randint(1, number)}```"
		except ValueError:
			choices = [c.strip() for c in data.split(",")]
			result = f"```\n{random.choice(choices)}```"
		
		
		embed = make_embed(
			ctx,
			description=result
		)
		
		await ctx.respond(embed=embed)
	
	
	@bridge_command(
		aliases=["b64", "64"],
		description="base64 encode/decode",
		usage="os.base64 >encode/decode >data",
		brief="os.b64 encode Hello world!\nos.64 decode SGVsbG8gd29ybGQh"
	)
	@option("mode", required=True, choices=["encode", "decode"])
	@option("data", required=True)
	async def base64(self, ctx, mode: str, *, data: str):
		databytes = data.encode("utf-8")
		result = b64encode(databytes) if mode == "encode" else b64decode(databytes)
		result = result.decode("utf-8")
		
		embed = make_embed(
			ctx,
			description=f"""```\n{mode}d "{data}"```"""
		)
		
		# so that the result can be copied to clipboard
		await ctx.respond(f"`{result}`", embed=embed)
	
	
	@bridge_command(
		aliases=["uni"],
		description="character to unicode / unicode to character",
		usage="os.unicode >character/unicode >unicode or any symbol",
		brief="os.unicode character 0097\nos.uni unicode a"
	)
	@option("data", description='example: 0097 or 97 (small letter "a") / • (U+2022)', required=True)
	@option("get", required=True, choices=["character", "unicode"])
	async def unicode(self, ctx, data: str, get: str):
		if get == "character":
			numbers = re.search(r"(\d+)", data).group()
			result = chr(int(numbers))
		else:
			code = ord(data[0])
			result = f"U+{code}"
		
		embed = make_embed(
			ctx,
			description=f"```\n{data} {get}```"
		)
		
		await ctx.respond(f"`{result}`", embed=embed)
	
	
	


def setup(bot):
	bot.add_cog(Utility(bot))