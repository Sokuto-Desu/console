import discord
import settings

from discord.ext.bridge import Bot

from db import DetaBase
from utils import make_embed

from traceback import format_exception


async def get_guild_prefix(bot: Bot | None, message):
	if test_mode:
		return "sudo." 
	
	prefixes_db = DetaBase("prefixes")
	
	guild_id = str(message.guild.id)
	
	guild_prefix = prefixes_db.get(guild_id, set_default=default_prefix)
	
	return guild_prefix

def get_traceback(error):
	"Returns formatted exception"
	return "".join(
		format_exception(
			type(error),
			error,
			error.__traceback__
		)
	)

async def handle_error(bot, ctx, error):
	"Checks some errors and replies respectively;"
	"else sends a traceback to the devserver."
	if isinstance(error, commands.MissingPermissions):
		return await reply(ctx, f"`error. {error.message.lower()}`")
	elif isinstance(error, commands.UserInputError):
		return await reply(ctx, f"`error. incorrect argument(s). {str(error).lower()}`")
	elif isinstance(error, commands.CommandNotFound):
		return
	
	
	traceback = get_traceback(error)
	embed = make_embed(
		ctx,
		title=f"**{ctx.guild}: {ctx.channel}: {ctx.author}**",
		description=f"```\n{traceback}```",
		color=0x151515
	)
	
	guild = bot.get_guild(settings.devserver)
	channel = guild.get_channel(settings.errors_channel)
	await channel.send(embed=embed)