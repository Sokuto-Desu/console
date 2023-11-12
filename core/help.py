import discord

from utils import make_embed
from settings import get_guild_prefix

from inspect import getfile

from discord import SelectOption, ComponentType
from discord.ui import Select, View
from discord.ext.commands import HelpCommand, Command
from discord.ext.bridge import BridgeExtCommand, BridgeCommandGroup


class ConsoleHelpCommand(HelpCommand):
	def command_not_found(self, command):
		return f"""`command "{command.qualified_name}" does not exist.`"""
	
	async def send_bot_help(self, mapping):
		ctx = self.context
		embed = make_embed(
			ctx,
			title="Help info.",
			# i made this description while being high i swear
			description=f"`Console is a bot made to serve utils for your server.`",
			thumbnail=dict(
				url=ctx.bot.user.avatar.url
			)
		)
		
		latency = ctx.bot.latency * 1000
		embed.add_field(name="Ping", value=f"{latency:.2f}ms ({latency}ms)")
		commands = f"{len(ctx.bot.commands)} commands"
		embed.add_field(name="Amount of commands", value=commands)
		
		dropdown = HelpDropdown(ctx.bot, embed)
		view = View()
		view.add_item(dropdown)
		
		await ctx.send(embed=embed, view=view)
	
	async def send_command_help(self, command):
		ctx = self.context
		
		embed = make_embed(
			ctx,
			title=f""""{command.qualified_name}" help.""",
			description=(
				"`> is required argument"
				"\n- is optional argument`"
			),
			thumbnail=dict(
				url=ctx.bot.user.avatar.url
			)
		)
		
		embed.add_field(name="Name", value=command.qualified_name)
		embed.add_field(name="Description", value=command.description)
		embed.add_field(name="Usage", value=command.usage)
		embed.add_field(name="Examples of usage", value=command.brief)
		
		await ctx.send(embed=embed)


class HelpDropdown(Select):
	def __init__(self, bot, og_embed: discord.Embed):
		super().__init__(
			placeholder="select the category you want to know about.",
			select_type=ComponentType.string_select
		)
		
		self.bot = bot
		self.cog_names = list(bot.cogs)
		self.og_embed = og_embed
		
		og_help = SelectOption(
			label="Bot info", 
			value="bot info",
			description="Info about the bot"
		)
		self.append_option(og_help)
		
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
		
		if choiced_cog == "bot info":
			return await interaction.response.edit_message(embed=self.og_embed)
		
		raw_cog = self.bot.cogs.get(choiced_cog)
		
		prefix = await get_guild_prefix(bot=None, message=interaction.channel)
		
		commands_list = []
		for command in raw_cog.walk_commands():
			if (
				isinstance(command, BridgeExtCommand | Command)
				and not hasattr(command, "walk_commands")
			):
				command_description = f"{prefix}{command.qualified_name} – {command.description}"
				commands_list.append(command_description)
		
		cog_commands = "\n".join(commands_list)
		
		embed = make_embed(
			interaction,
			title=f"{choiced_cog}.",
			description=(
				f"""`use "{prefix}help >your_command" for more info about specific command.`"""
				f"\n\n```\n{cog_commands}```"
			)
		)
		
		await interaction.response.edit_message(embed=embed, view=self.view)
