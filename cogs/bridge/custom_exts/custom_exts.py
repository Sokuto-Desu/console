from utils import reply
from db import DetaBase
from core.assets import get_guild_prefix

from discord.ext.commands import Cog
from discord.ext.bridge import bridge_group, BridgeExtCommand
from discord import option, default_permissions

# see format.txt for how commands are stored in DB

class CustomCommands(
	Cog,
	name="Custom commands",
	description="Create your own custom prefix commands"
):
	def __init__(self, bot):
		self.bot = bot
		self.db = DetaBase(base_name="custom_exts")
	
	
	@bridge_group(description="custom commands")
	async def exts(self, ctx):
		pass
	
	@exts.command(
		name="create",
		description="create custom command",
		usage="os.exts create >command_name >command callback",
		brief="os.exts create test Hello World!"
	)
	@option("name", description="command's name", required=True)
	@option("callback", description="command's callback (what to reply)", required=True)
	@default_permissions(manage_messages=True)
	async def _create(self, ctx, name: str, *, callback: str):
		guild_id = str(ctx.guild.id)
		custom_commands = self.db.get(guild_id, set_default=[])
		
		already_exists = tuple(
			filter(
				lambda cmd: cmd.get("name") == name,
				custom_commands
			
		) if custom_commands else False
		
		bot_command_names = tuple(
			map(
				lambda c: c.name,
				filter(
					# check if the command is ext commanddd
					lambda c: isinstance(c, BridgeExtCommand), 
					self.bot.commands
				)
			)
		)
		
		if already_exists or name in bot_command_names:
			return await reply(ctx, "`this command already exists.`")
		
		new_command = {
			"name": name,
			"callback": callback
		}
		custom_commands.append(new_command)
		
		self.db.set(key=guild_id, value=custom_commands)
		
		await reply(ctx, 
			"`successfully created ext (prefix) command with these parameters:"
			f"\nname: {name}"
			f"\ncallback: {callback}`"
		)
	
	
	@exts.command(
		name="delete",
		description="delete custom command",
		usage="os.exts delete >command_name",
		brief="os.exts delete test"
	)
	@option("name", description="name of custom command", required=True)
	@default_permissions(manage_messages=True)
	async def _delete(self, ctx, name: str):
		guild_id = str(ctx.guild.id)
		custom_commands = self.db.get(guild_id, set_default=[])
		
		command = tuple(filter(
			lambda cmd: cmd.get("name") == name,
			custom_commands
		))[0] if custom_commands else False
		
		if not command:
			return await reply(ctx, "`this custom command does not exist.`")
		
		commands_list = custom_commands.remove(command)
		
		self.db.set(key=guild_id, value=commands_list)
		
		await reply(ctx, f"""`successfully deleted ext (prefix) command "{name}"`""")
	
	
	@Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return
		
		prefix = await self.bot.get_prefix(message)
		
		if message.content.startswith(prefix):
			# remove prefix
			command_name = message.content.removeprefix(prefix) 
			# remove everything after first space (getting command name)
			command_name = command_name.split(" ", 1)[0] 
			
			guild_id = str(message.guild.id)
			
			custom_commands = self.db.get(guild_id)
			command = tuple(filter(
				lambda cmd: cmd.get("name") == command_name,
				custom_commands or [{}]
			))
			
			if cmd := command:
				await message.channel.send(cmd[0].get("callback"))


def setup(bot):
	bot.add_cog(CustomCommands(bot))