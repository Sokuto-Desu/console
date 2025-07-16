import discord, os

from discord.ext import commands
from discord.ext.bridge import Bot

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
		
		self.bot_cogs = ["cogs.slash.echo.echo"]
		
		for cog in self.bot_cogs:
			self.load_extension(cog)
	
	async def on_ready(self):
		print(f"logged in.\nuser: {self.user}")
	
	def run(self):
		super().run(os.getenv("TOKEN"))