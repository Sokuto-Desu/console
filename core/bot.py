import settings
import discord

from discord.ext import commands
from discord.ext.bridge import Bot

from sys import argv
from utils import make_embed, handle_error
from traceback import format_exception
from asyncio import sleep


class ConsoleBot(Bot):
	def __init__(self):
		super().__init__(
			command_prefix = settings.prefix,
			intents = discord.Intents.all(),
			case_insensitive = True,
			activity = discord.Activity(
				type = discord.ActivityType.watching,
				name = settings.activity
			)
		)
		
		self.is_test = settings.is_test if not "-t" in argv else True
		self.to_load = settings.cogs + settings.cogs_slash
		
		for cog in self.to_load:
			self.load_extension(cog)
	
	
	async def on_application_command_error(self, ctx, error):
		await handle_error(self, ctx, error)
	
	async def on_command_error(self, ctx, error):
		await handle_error(self, ctx, error)
	
	
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