import settings
import discord

from discord.ext import commands
from discord.ext.bridge import Bot

from sys import argv, exit
from asyncio import sleep
from utils import handle_error
from .help import ConsoleHelpCommand


class ConsoleBot(Bot):
	def __init__(self):
		super().__init__(
			command_prefix = settings.get_guild_prefix,
			intents = discord.Intents.all(),
			activity = settings.activity,
			owner_ids = settings.owners,
			help_command = ConsoleHelpCommand(),
			case_insensitive = True,
			strip_after_prefix = True
		)
		
		self.is_test = settings.test_mode if not "-t" in argv else True
		self.cogs_to_load = settings.bridge_cogs + settings.slash_cogs
		
		for cog in self.cogs_to_load:
			self.load_extension(cog)
	
	
	async def on_application_command_error(self, ctx, error) -> None:
		await handle_error(self, ctx, error)
	
	async def on_command_error(self, ctx, error) -> None:
		await handle_error(self, ctx, error)
	
	
	async def on_connect(self) -> None:
		if "-s" in argv:
			await self.sync_commands()
			print("commands synced.")
	
	async def on_ready(self) -> None:
		print("-"*25)
		print(f"logged in as {self.user}.")
		print(f"test mode: {str(self.is_test).lower()}.")
		print("-"*25)
		
		if "-f" in argv:
			await sleep(1)
			await self.close()
	
	
	def run(self) -> None:
		if self.is_test:
			super().run(settings.test_token)
		else:
			super().run(settings.token)