import settings
from sys import argv
from .utils import Embed
from traceback import format_exception
from asyncio import sleep

import discord
from discord.ext import commands


class ConsoleBot(discord.Bot):
 	def __init__(self):
 		super().__init__(
#			command_prefix = settings.prefix,
 			intents = discord.Intents.all(),
 			case_insensitive = True,
 			activity = discord.Activity(
 				type = discord.ActivityType.watching,
 				name = settings.activity
 			)
 		)
 		
 		self.is_test = settings.is_test if not "-t" in argv else True
 		self.to_load = settings.cogs
 		
 		for cog in self.to_load:
 			self.load_extension(cog)
 	
 	
 	async def on_application_command_error(self, ctx, error):
 		if isinstance(error, commands.MissingPermissions):
 			return await ctx.respond(f"`error. {error.message.lower()}`")
 		
 		elif isinstance(error, commands.UserInputError):
 			return await ctx.respond(f"`error. incorrect argument(s). {error.message.lower()}`")
 		
 		
 		traceback = "".join(format_exception(type(error), error, error.__traceback__))
 		embed = Embed(
 			title = f"**{ctx.guild}**: **{ctx.channel}**: **{ctx.author}**",
 			description = f"```\n{traceback}```"
 		)
 		
 		channel = self.get_guild(settings.devserver).get_channel(settings.errors_channel)
 		await channel.send(embed = embed)
 	
 	async def on_connect(self):
 		if "-s" in argv:
 			await self.sync_commands()
 			print("commands synced.")
 	
 	async def on_ready(self):
 		print("-"*25)
 		print(f"logged in as {self.user}.")
 		print(f"test mode: {str(self.is_test).lower()}.")
 		print("-"*25)
 		
 		if "-f" in argv:
 			await sleep(1)
 			await self.close()
 	
 	
 	def run(self):
 		if self.is_test:
 			return super().run(settings.test_token)
 		super().run(settings.token)
