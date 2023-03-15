from asyncio import sleep
from discord import Message


async def reply(ctx, *args, **kwargs):
	if ctx.is_app:
		await ctx.respond(*args, **kwargs)
	else:
		await ctx.send(*args, **kwargs)

async def close(message: Message, time: int=5):
	await sleep(time)
	await message.delete()

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


async def str_to_bool(arg):
	return True if arg.lower() == "true" else False