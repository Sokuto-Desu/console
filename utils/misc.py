import settings

from asyncio import sleep
from traceback import format_exception

from discord import Message, Embed, ApplicationContext
from discord.ext import commands


async def reply(ctx, *args, **kwargs):
	try:
		if ctx.is_app:
			return await ctx.respond(*args, **kwargs)
		else:
			return await ctx.send(*args, **kwargs)
	
	except AttributeError:
		if isinstance(ctx, ApplicationContext):
			return await ctx.respond(*args, **kwargs)
		else:
			return await ctx.send(*args, **kwargs)


# converts time (8m, 1h, 2d, etc.) to seconds
async def convert_time(time):
	time_list = re.split('(\d+)', time)
	if time_list[2] == "s":
		seconds = int(time_list[1])
	if time_list[2] == "m":
		seconds = int(time_list[1]) * 60
	if time_list[2] == "h":
		seconds = int(time_list[1]) * 60 * 60
	if time_list[2] == "d":
		seconds = int(time_list[1]) * 60 * 60 * 24
	
	return times


# formats exception
def get_traceback(error):
	return "".join(
		format_exception(
			type(error),
			error,
			error.__traceback__
		))

# used for handling errors in bot.py
async def handle_error(bot, ctx, error):
	if isinstance(error, commands.MissingPermissions):
		return await reply(f"`error. {error.message.lower()}`")
	elif isinstance(error, commands.UserInputError):
		return await reply(f"`error. incorrect argument(s). {str(error).lower()}`")
	elif isinstance(error, commands.CommandNotFound):
		return
	
	
	traceback = "".join(get_traceback(error))
	embed = Embed( # usually i use make_embed but circular import prevents me from it here
		title=f"**{ctx.guild}: {ctx.channel}: {ctx.author}**",
		description=f"```\n{traceback}```",
		color=0x151515
	)
	
	guild = bot.get_guild(settings.devserver)
	channel = guild.get_channel(settings.errors_channel)
	await channel.send(embed=embed)