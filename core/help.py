from discord.ext.cmmands import HelpCommand

class ConsoleHelp(HelpCommand):
	async def send_bot_help(self, mapping):
		for cog, commands in mapping.items():
			