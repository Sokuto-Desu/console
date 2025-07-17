from discord.ext import commands

from common import config, formatters

# used to handle errors in bot.py
async def handle_error(bot, ctx, error):
	"Checks some errors and replies respectively;"
	"else sends a traceback to the devserver."
	if isinstance(error, commands.MissingPermissions):
		return await formatters.reply(ctx, f"`error. {error.message.lower()}`")
	elif isinstance(error, commands.UserInputError):
		return await formatters.reply(ctx, f"`error. incorrect argument(s). {str(error).lower()}`")
	elif isinstance(error, commands.CommandNotFound):
		return
	
	traceback = formatters.get_traceback(error)
	
	embed = formatters.make_embed( 
		ctx,
		title=f"Server: {ctx.guild}\nChannel: {ctx.channel}\nBy: {ctx.author or ctx.user}**",
		description=f"```\n{traceback}```",
	)
	
	channel = bot.get_guild(config.developer_server).get_channel(config.exceptions_channel)
	await channel.send(embed=embed)