from utils import make_embed, ChatGPT
from random import choice, randint
from base64 import b64decode, b64encode
from asyncio import wait_for, TimeoutError

from discord.ext.commands import Cog, MemberConverter, command
from discord.ext.bridge import bridge_command
from discord import option


class Utility(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	
	@bridge_command(description="get member avatar", usage="os.avatar n>member", brief="os.avatar @Console#3862")
	@option("member", required=False, default=None)
	async def avatar(self, ctx, member: MemberConverter=None):
		member = ctx.author if member is None else member
		
		embed = make_embed(
			title = f"`{member}'s avatar`",
			image = {"url": member.avatar.url}
		)
		await ctx.respond(embed = embed)
	
	
	@bridge_command(description="random choice", usage="os.random r>number or choices", brief="os.random yes, no, probably // os.random 10")
	@option("data", description="choice1, choice2, choice3 ... (random choice) | any number (random number choice)", required=True)
	async def random(self, ctx, *, data: str):
		try:
			number = int(data)
			return await ctx.respond(f"`{randint(1, number)}`")
		except ValueError:
			pass
		
		choices = [c.strip() for c in data.split(",")]
		
		await ctx.respond(f"`{choice(choices)}`")
	
	
	@bridge_command(aliases=["b64", "64"], description="base64 encode/decode", usage="os.b")
	@option("mode", required=True, choices=["encode", "decode"])
	@option("data", required=True)
	async def base64(self, ctx, mode: str, data: str):
		databytes = data.encode("utf-8")
		result = b64encode(databytes) if mode == "encode" else b64decode(databytes)
		result = result.decode("utf-8")
		
		await ctx.respond(f"`{result}`")
	
	
	@bridge_command(description="character to unicode / unicode to character")
	@option("get", required=True, choices=["character", "unicode"])
	@option("data", description='example: 0097 or 97 (small letter "a") | • (U+2022)', required=True)
	async def unicode(self, ctx, get: str, data: str):
		if get == "character":
			result = chr(int(data))
		else:
			code = ord(data[0])
			result = f"U+{code}"
		
		await ctx.respond(f"`{result}`")
	
	@command(aliases=["chat"])
	async def chatgpt(self, ctx, *, prompt):
		message = await ctx.send("`please wait a minute.`")
		
		chatgpt = ChatGPT(ctx.author.id)
		
		try:
			completion = await wait_for(chatgpt.prompt(prompt), timeout=150)
		except TimeoutError:
			return await message.edit("`sorry, there was an unknown error. try again later.`")
		
		result = []
		for i in range(0, len(completion), 1980):
			result.append(completion[i:i+1980])
		
		await message.edit(f"`[conversation limit: {chatgpt.user_limit_status}]`\n{result.pop(0)}")
		for content in result:
			await ctx.send(f"`{content}")


def setup(bot):
	bot.add_cog(Utility(bot))