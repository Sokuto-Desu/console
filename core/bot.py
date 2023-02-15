import discord

import settings
from .utils import handle_error


class ConsoleBot(discord.Bot):
 	def __init__(self):
 		super().__init__(
#		command_prefix = settings.config["prefix"],
 		intents = discord.Intents.all(),
 		case_insensitive = True,
 		activity = discord.Activity(
 			type = discord.ActivityType.watching,
 			name = settings.config["activity"]
 			)
 		)
 		
 		self.is_test = settings.config["is_test"]
 		self.to_load = settings.cogs
 		
 		for cog in self.to_load:
 			self.load_extension(cog)
 	
 	async def on_application_command_error(self, ctx, error):
 		await handle_error(ctx, error)
 	
 	
 	async def on_ready(self):
 		print("-"*25)
 		print(f"Logged in as {self.user} (test mode: {str(self.is_test).lower()})")
 		print("-"*25)
 	
 	def run(self):
 		if self.is_test:
 			return super().run(settings.config["test_token"])
 		super().run(settings.config["token"])