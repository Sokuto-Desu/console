import discord
import settings, utils


class ConsoleBot(commands.Bot):
	def __init__(self):
		super().__init__(
		command_prefix = settings.config["prefix"],
		intents = discord.Intents.all(),
		case_insensitive = True,
		activity = discord.Activity(
			type = discord.ActivityType.watching,
			name = settings.config["activity"]
			)
		)
		
		self.is_test = settings.config["is_test"]
		self.cogs = settings.cogs
		
		for cog in self.cogs:
			self.load_extension(cog)
	
	async def on_application_command_error(self, ctx, error):
		await utils.handle_error(ctx, error)
	
	
	async def on_ready(self):
		print("-"*25)
		print(f"Logged in as {self.user} (test mode: {self.is_test.lower()})")
		print("-"*25)
	
	def run(self):
		if self.is_test:
			return super().run(settings.config["token"])
		super().run(settings.config["test_token"])