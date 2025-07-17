import discord

from discord.ext.bridge import Bot

from common import config

from . import handling


class BotClass(Bot):
	def __init__(self):
		super().__init__(
			command_prefix = config.get_guild_prefix,
			intents = discord.Intents.all(),
			activity = config.activity,
			case_insensitive = True,
			strip_after_prefix = True
		)
		
		cogs = config.get_cogs()
		
		for cog in cogs:
			try:
				self.load_extension(cog)
			except discord.errors.ExtensionNotFound:
				continue
	
	async def on_application_command_error(self, ctx, error):
		await handling.handle_error(self, ctx, error)
	
	async def on_command_error(self, ctx, error):
		await handling.handle_error(self, ctx, error)
	
	async def on_ready(self):
		print(f"logged in.\nuser: {self.user}")
	
	def run(self):
		if config.test_mode:
			super().run(config.test_token)
		else:
			super().run(config.token)