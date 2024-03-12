import discord

from db import DetaBase
from asyncio import sleep
from typing import Union

from discord import option, TextChannel, ForumChannel, CategoryChannel, Thread, default_permissions
from discord.ext.commands import Cog
from discord.ext.bridge import bridge_group

from utils import make_embed, reply
from core.assets import get_guild_prefix


class Filter(
	Cog,
	name="Message filter",
	description="Delete messages containing bad/unwanted words after a given amount of time"
):
	def __init__(self, bot):
		self.bot = bot
		self.db = DetaBase("message_filter")
	
	
	@Cog.listener()
	async def on_message(self, message):
		prefix = await get_guild_prefix(self.bot, message)
		if message.author.bot or message.content.startswith(f"{prefix}filter"):
			return
		
		# do NOT unseparate these two if statements
		blacklist = self.db.get(str(message.guild.id))
		if not blacklist:
			return
		
		# blacklist is a list of dicts
		for word in blacklist:
			if word["name"] in message.content.lower():
				await sleep(word["wait"])
				
				if channel := word["channel"]:
					channel_id = int(channel)
				else:
					channel_id = None
				
				if (
					not channel_id or channel_id == message.channel.id 
					or (isinstance(message.channel, Thread) and message.channel.parent.id == word["channel"]) 
					or channel_id == message.channel.category.id
				): 
					await message.delete()
	
	
	@bridge_group(description="filter words/symbols in chat")
	async def filter(self, ctx):
		pass
	
	@filter.command(
		description="add words/symbols to filter blacklist",
		usage="os.filter add >word >wait_before_delete_(in_seconds) >channel",
		brief="os.filter add N-word // os.filter add bad_word 0 #general"
	)
	@option("word", description="word/symbol to be blacklisted",
			required=True)
	@option("wait", description="how long to wait before deleting message (in seconds)",
			required=False, default=0)
	@option("channel", description="in which channel to delete messages (leave blank to apply to the entire server)",
			required=False, default=None)
	@default_permissions(manage_messages=True)
	async def add(
		self, 
		ctx, 
		word: str, 
		wait: float=0, 
		channel: Union[TextChannel, Union[ForumChannel, CategoryChannel]]=None
	):
		guild_id = str(ctx.guild.id)
		blacklist = self.db.get(guild_id)
		blacklist = [] if not blacklist else blacklist
		element = {
			"name": word,
			"wait": wait,
			"channel": str(channel.id) if channel else None
		}
		
		if not element in blacklist:
			blacklist.append(element)
			
			self.db.set(key=str(ctx.guild.id), value=blacklist)
			
			response = f"""successfully added "{word}" to a blacklist."""
		else:
			response = "this word is already in a blacklist."
		
		embed = make_embed(
			ctx,
			description=f"```\n{response}```"
		)
		
		await reply(ctx, embed=embed)
	
	
	@filter.command(
		aliases=["delete"],
		description="remove words/symbols from filter blacklist",
		usage="os.filter remove >word",
		brief="os.filter remove accidentally_added_word // os.filter remove foo"
	)
	@option("word", description="word/symbol to be removed from blacklist",
			required=True)
	@default_permissions(manage_messages=True)
	async def remove(self, ctx, word: str):
		guild_id = str(ctx.guild.id)
		blacklist = self.db.get(guild_id)
		if not blacklist:
			response = "this word isn't in a blacklist."
		else:
			element = [item for item in blacklist if item["name"] == word]
			
			if not element:
				response = "this word isn't in a blacklist."
			else:
				blacklist.remove(element[0])
				
				self.db.set(key=str(ctx.guild.id), value=blacklist)
				
				response = f"""successfully removed "{word}" from a blacklist."""
		
		embed = make_embed(
			ctx,
			description=f"```\n{response}```"
		)
		
		await reply(ctx, embed=embed)
	
	@filter.command(
		aliases=["show", "showall"],
		description="show filter blacklist",
		usage="os.filter list",
		brief="os.filter show // os.filter showall"
	)
	@option("word", description="word/symbol to show info about",
			required=False, default=None)
	async def list(self, ctx, word: str=None):
		guild_id = str(ctx.guild.id)
		blacklist = self.db.get(guild_id)
		
		if not blacklist:
			response = "filter blacklist is empty."
		
		elif not word:
			words_list = [item.get("name") for item in blacklist]
			result = "\n".join(words_list)
			
			response = f"message filter blacklist:\n{result}"
		
		else:
			element = discord.utils.find(lambda item: item.get("name") == word, blscklist)
			if not element:
				response = "this word isn't in blacklist."
			else:
				channel = element[0].get("channel")
				channel_info = f"<#{int(channel)}>" if channel else "whole server"
				
				word_info = (
					f"name: {element[0]['name']}"
					f"\nwait time: {element[0]['wait']}"
					f"\nwhere to delete: {channel_info}"
				)
				
				response = f'"{word}" info:\n\n{word_info}'
		
		embed = make_embed(
			ctx,
			description=f"```\n{response}```"
		)
		
		await reply(ctx, embed=embed)


def setup(bot):
	bot.add_cog(Filter(bot))

"""
[
	{
		"name": "bad_word",
		"channel": some_channel_id,
		"wait": 0
	},
	{
		"name": "not_a_bad_word_but_needs_to_be_deleted",
		"channel": some_channel_id,
		"wait": 15
	}
]
"""