import settings
import datetime

from asyncio import sleep

from discord import Message, Embed, ApplicationContext
from discord.ext import commands


async def reply(ctx, *args, **kwargs):
	"Replies in the given context both on slash and ext commands;"
	"you should always use this in bridge commands unless you want BridgeContext.respond (which uses .reply() for ext context, not .send())"
	if isinstance(ctx, ApplicationContext):
		return await ctx.respond(*args, **kwargs)
	else:
		return await ctx.send(*args, **kwargs)


def convert_time(time):
	"Converts time in a %d%c format to seconds"
	time_list = re.split('(\d+)', time)
	if time_list[2] == "s":
		seconds = int(time_list[1])
	if time_list[2] == "m":
		seconds = int(time_list[1]) * 60
	if time_list[2] == "h":
		seconds = int(time_list[1]) * 60 * 60
	if time_list[2] == "d":
		seconds = int(time_list[1]) * 60 * 60 * 24
	
	return seconds

def format_time(time: datetime.datetime):
	"Formats datetime object as given below;"
	"e.g. Monday, 17/01/2016 22:18:03.672 (UTC+0000)"
	formatted_time = time.strftime("%A, %d/%m/%Y %H:%M:%S.%f (%Z%z)")
	return formatted_time
