import discord, os

from discord.ext import commands
from discord.ext.bridge import Bot

from . import config

from sys import argv
from dotenv import load_dotenv

load_dotenv()

class BotClass(Bot):
	def __init__(self):
		super().__init__(
			command_prefix = "os.",
			intents = discord.Intents.all(),
			case_insensitive = True,
			strip_after_prefix = True
		)
		
		cogs = config.get_cogs()
		
		for cog in cogs:
			try:
				self.load_extension(cog)
			except discord.errors.ExtensionNotFound:
				continue
	
	async def on_ready(self):
		print(f"logged in.\nuser: {self.user}")
	
	def run(self):
		if "-t" in argv:
			super().run(config.test_token)
		else:
			super().run(config.token)