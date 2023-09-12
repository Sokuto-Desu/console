from utils import Database
from asyncio import sleep
from typing import Union

from discord import option, TextChannel, ForumChannel, CategoryChannel, Thread, default_permissions
from discord.ext.commands import Cog
from discord.commands import SlashCommandGroup


class Filter(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.filter_db = Database("message_filter")
	
	
	@Cog.listener()
	async def on_message(self, message):
		blacklist = self.filter_db.get(str(message.guild.id))
		
		if not blacklist or message.author.bot:
			return
		
		if blacklist != []: # blacklist is list of dicts
			for word in blacklist:
				if word["name"] in message.content.lower():
					await sleep(word["wait"])
					if channel := word["channel"]:
						channel_id = int(channel)
					else:
						channel_id = None
					
					if (not channel_id or channel_id == message.channel.id # whole server or specific channel
						or (isinstance(message.channel, Thread) and message.channel.parent.id == word["channel"]) # threads
						or channel_id == message.channel.category.id): # categories
						await message.delete()
	
	
	filter = SlashCommandGroup("filter", "filter words/symbols in chat")
	
	@filter.command(description="add words/symbols to filter blacklist")
	@option("word", description="word/symbol to be blacklisted",
			required=True)
	@option("wait", description="how long to wait before deleting message (in seconds)",
			required=False, default=0)
	@option("channel", description="in which channel to delete messages (leave blank to apply to the entire server)",
			required=False, default=None)
	@default_permissions(manage_messages=True)
	async def add(self, ctx, word: str, wait: float, channel: Union[TextChannel, Union[ForumChannel, CategoryChannel]]):
		blacklist = self.filter_db.get(str(ctx.guild.id))
		blacklist = [] if not blacklist else blacklist
		element = {
			"name": word,
			"wait": wait,
			"channel": str(channel.id) if channel else None
		}
		
		if not element in blacklist:
			blacklist.append(element)
		else:
			await ctx.respond("`this word is already in blacklist.`")
		
		self.filter_db.set(key=str(ctx.guild.id), value=blacklist)
		
		await ctx.respond(f"""`successfully added "{word}" to blacklist.`""")
	
	
	@filter.command(description="remove words/symbols from filter blacklist")
	@option("word", description="word/symbol to be removed from blacklist",
			required=True)
	@default_permissions(manage_messages=True)
	async def remove(self, ctx, word: str):
		blacklist = self.filter_db.get(str(ctx.guild.id))
		if not blacklist:
			await ctx.respond("`this word isn't in blacklist.`")
		
		element = [item for item in blacklist if item["name"] == word]
		
		if element:
			blacklist.remove(element[0])
			self.filter_db.set(key=str(ctx.guild.id), value=blacklist)
			
			await ctx.respond(f"""`successfully removed "{word}" from blacklist.`""")
		else:
			await ctx.respond("`this word isn't in blacklist.`")
	
	@filter.command(description="show filter blacklist")
	@option("word", description="word/symbol to show info",
			required=False, default=None)
	async def list(self, ctx, word: str):
		blacklist = self.filter_db.get(str(ctx.guild.id))
		
		if blacklist == [] or not blacklist:
			return await ctx.respond("`filter blacklist is empty.`")
		
		if not word:
			words_list = [item["name"] for item in blacklist]
			result = "\n".join(words_list)
			
			await ctx.respond(f"`message filter blacklist:\n{result}`")
		else:
			element = [item for item in blacklist if item["name"] == word]
			if element == []:
				await ctx.respond("`this word isn't in blacklist.`")
			else:
				channel = element[0]["channel"]
				channel_info = f"<#{int(channel)}>" if channel else "whole server"
				
				word_info = (
					f"name: {element[0]['name']}\n"
					f"wait time: {element[0]['wait']}\n"
					f"where to delete: `{channel_info}"
				)
				
				await ctx.respond(f'`"{word}" info:\n\n{word_info}')


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