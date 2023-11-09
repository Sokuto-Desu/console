import discord

from utils import make_embed
from settings import get_guild_prefix

from inspect import getfile

from discord import SelectOption, ComponentType
from discord.ui import Select, View
from discord.ext.commands import HelpCommand
from discord.ext.bridge import BridgeExtCommand, BridgeCommandGroup


class ConsoleHelpCommand(HelpCommand):
	async def send_bot_help(self, mapping):
		ctx = self.context
		embed = make_embed(
			ctx,
			title="`help info.`",
			# i made this description while being high i swear
			description="`console is a bot made to serve utils for your server.`",
			thumbnail=dict(
				url=ctx.bot.user.avatar.url
			)
		)
		
		dropdown = HelpDropdown(ctx.bot)
		view = View()
		view.add_item(dropdown)
		
		await ctx.send(embed=embed, view=view)


class HelpDropdown(Select):
	def __init__(self, bot):
		super().__init__(
			placeholder="select the category you want to know about.",
			select_type=ComponentType.string_select
		)
		
		self.bot = bot
		self.cog_names = list(bot.cogs)
		
		
		for cog_name in self.cog_names:
			raw_cog = bot.cogs.get(cog_name)
			
			# checks if cog is a developer cog or a slash cog (by finding the filepath of it)
			if cog_name == "developer" or "slash" in getfile(raw_cog.__class__):
				continue
			
			cog_description = raw_cog.description or "category description not provided."
			cog_option = SelectOption(
				label=cog_name,
				value=cog_name,
				description=cog_description
			)
			
			self.append_option(cog_option)
	
	async def callback(self, interaction):
		choiced_cog = self.values[0]
		
		raw_cog = self.bot.cogs.get(choiced_cog)
		
		prefix = await get_guild_prefix(bot=None, message=interaction.channel)
		
		commands_list = []
		for command in raw_cog.walk_commands():
			if isinstance(command, BridgeExtCommand) and not hasattr(command, "walk_commands"):
				command_description = f"{prefix}{command.qualified_name} – {command.description}"
				commands_list.append(command_description)
		
		cog_commands = "\n".join(commands_list)
		
		embed = make_embed(
			interaction,
			title=f"`{choiced_cog} commands.`",
			description=(
				f"""`use "{prefix}help >your_command" for more info about specific command.`"""
				f"\n\n```\n{cog_commands}```"
			)
		)
		
		await interaction.response.edit_message(embed=embed, view=self.view)
