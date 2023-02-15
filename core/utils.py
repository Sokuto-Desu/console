import settings
from traceback import format_exception

# embed with default color 0x151515 (black)
class Embed(discord.Embed):
	def __init__(self, **kwargs):
		super().__init__(color = 0x151515, kwargs)


# "closes" window (waits time and deletes message)
async def close(message: discord.Message, time: int = 5):
	await asyncio.sleep(time)
	await message.delete()

# converts time (8m, 1h, 2d, etc.) to seconds
async def convert_time(time):
	time_list = re.split('(\d+)', time)
	if time_list[2] == "s":
		times = int(time_list[1])
	if time_list[2] == "m":
		times = int(time_list[1]) * 60
	if time_list[2] == "h":
		times = int(time_list[1]) * 60 * 60
	if time_list[2] == "d":
		times = int(time_list[1]) * 60 * 60 * 24
	
	return times


# every command error goes here (see on_application_command_error event in bot.py)
async def handle_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		return await ctx.respond(f"`error. {error.message.lower()}`")
	elif isinstance(error, commands.UserInputError):
		return await ctx.respond(f"`error. incorrect argument(s). {error.message.lower()}`")
	
	traceback = "".join(format_exception(type(error), error, error.__traceback__))
	embed = discord.Embed(
		title = f"**{ctx.guild}**: **{ctx.channel}**: **{ctx.author}**",
		description = f"```\n{traceback}```",
		color = 0x151515
	)
	
	channel = settings.config["errors_channel"]
	message = await channel.send(embed = embed)