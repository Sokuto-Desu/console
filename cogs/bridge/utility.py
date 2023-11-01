import re, asyncio

from utils import make_embed, GPT, reply
from random import choice, randint
from base64 import b64decode, b64encode

from discord.ext.commands import Cog
from discord.ext.bridge import bridge_command
from discord import option, Member


class Utility(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	
	@bridge_command(
		description="get member avatar",
		usage="os.avatar -member", 
		brief="os.avatar @Console#3862"
	)
	@option("member", required=False, default=None)
	async def avatar(self, ctx, member: Member=None):
		member = member or ctx.author
		
		embed = make_embed(
			title = f"`{member}'s avatar`",
			image = {"url": member.avatar.url}
		)
		await ctx.respond(embed = embed)
	
	
	@bridge_command(
		aliases=["r"],
		description="random choice",
		usage="os.random >number or choices",
		brief="os.random yes, no, probably // os.random 10"
	)
	@option("data", description="choice1, choice2, choice3 ... (random choice) | any number (random number choice)", required=True)
	async def random(self, ctx, *, data: str):
		try:
			number = int(data)
			return await ctx.respond(f"`{randint(1, number)}`")
		except ValueError:
			pass
		
		choices = [c.strip() for c in data.split(",")]
		
		await ctx.respond(f"`{choice(choices)}`")
	
	
	@bridge_command(
		aliases=["b64", "64"],
		description="base64 encode/decode",
		usage="os.base64 >encode/decode >data",
		brief="os.b64 encode Hello world! // os.64 decode SGVsbG8gd29ybGQh"
	)
	@option("mode", required=True, choices=["encode", "decode"])
	@option("data", required=True)
	async def base64(self, ctx, mode: str, *, data: str):
		databytes = data.encode("utf-8")
		result = b64encode(databytes) if mode == "encode" else b64decode(databytes)
		result = result.decode("utf-8")
		
		await ctx.respond(f"`{result}`")
	
	
	@bridge_command(
		aliases=["uni"],
		description="character to unicode / unicode to character",
		usage="os.unicode >character/unicode >unicode or any symbol",
		brief="os.unicode character 0097 // os.uni unicode a"
	)
	@option("get", required=True, choices=["character", "unicode"])
	@option("data", description='example: 0097 or 97 (small letter "a") | • (U+2022)', required=True)
	async def unicode(self, ctx, get: str, data: str):
		if get == "character":
			numbers = re.search(r"(\d+)", data).group()
			result = chr(int(numbers))
		else:
			code = ord(data[0])
			result = f"U+{code}"
		
		await ctx.respond(f"`{result}`")
	
	
	@bridge_command(
		aliases=["chatgpt", "chat"],
		description=(
			"talk to chatgpt (gpt-3.5). "
			"note: if console doesn't answer for a long time just run command again."
		),
		usage="os.chatgpt >prompt",
		brief="os.chatgpt Hello"
	)
	@option("prompt", required=True)
	async def gpt(self, ctx, *, prompt: str):
		message = await reply(ctx, content="`please wait a minute. prompt is processing.`")
		
		gpt35 = GPT(ctx.author.id)
		
		try:
			completion = await asyncio.wait_for(gpt35.prompt(prompt), timeout=150)
		except asyncio.TimeoutError:
			return await message.edit("`sorry, there was an unknown error. try again later.`")
		
		# split the content to fit in the discord limit of characters
		result = []
		for i in range(0, len(completion), 1980):
			result.append(completion[i:i+1980])
		
		await message.edit(f"`GPT-3.5`\n{result.pop(0)}")
		for content in result:
			await ctx.send(f"`{content}")
	
	@bridge_command(
		aliases=["chatgpt-erase", "chat-erase", "erase_dialogue", "erase-chat", "erase-chatgpt", "erase-gpt", "erase_conversation", "ed"],
		description="erase dialogue with gpt-3.5",
		usage="os.gpt_erase_dialogue",
		brief="os.ed"
	)
	async def gpt_erase_dialogue(self, ctx):
		gpt35 = GPT(ctx.author.id)
		await gpt35.erase_dialogue()
		
		await reply(ctx, "`dialogue erased.`")


def setup(bot):
	bot.add_cog(Utility(bot))