from utils import make_embed
from difflib import get_close_matches

from discord import SelectOption
from discord.ui import Select, View
from discord.ext.commands import HelpCommand


class ConsoleHelpCommand(HelpCommand):
	async def send_bot_help(self, mapping):
		for cog, commands in mapping.items():
			pass


class HelpDropdown(Select):
	def __init__(self, options: list, bot_cogs: list):
		super().__init__(
			placeholder="select the module you want to know about."
			options=options
		)
		self.bot_cogs = bot_cogs
	
	async def callback(self, inter):
		choice = self.values[0].lower()
		cogs_names_list = [cog.qualified_name.lower() 
							for cog in self.bot_cogs]
		
		if not choice in cogs_names_list:
			similar = get_close_matches(choice, cogs_names_list)
			await inter.response.send_message(f"`there is no such module.\ndid you mean {similar}?`")
		else:
			commands_list = []
			for 
			
			embed = make_embed(
				title=f"`{choice} commands.`"
			)