import discord

from discord import Embed
from discord.ext import commands

from datetime import datetime
from traceback import format_exception


async def reply(ctx, *args, **kwargs):
	"""
	Replies in the given context both in slash and ext commands;
	you should always use this in bridge commands unless you specifically want BridgeContext.respond
	(which uses .reply() for ext context, not .send())
	"""
	if isinstance(ctx, discord.ApplicationContext):
		return await ctx.respond(*args, **kwargs)
	else:
		return await ctx.send(*args, **kwargs)


def format_time(time: datetime):
	"Formats a datetime object like this:"
	"Monday, 17/01/2016 22:18:03.672 (UTC+0000)"
	formatted_time = time.strftime("%A, %d/%m/%Y %H:%M:%S.%f (%Z%z)")
	return formatted_time


def get_traceback(error):
	"Returns the formatted exception"
	return "".join(
		format_exception(
			type(error),
			error,
			error.__traceback__
		)
	)


def make_embed(ctx, **parameters) -> Embed:
	"""
	Embed generator. 
	Automatically places a footer with the message info. 
	Defaults the color to 0x151515.
	"""
	# i dont know why i did this but its needed 
	for parameter in ("footer", "title", "description"):
		if parameters.get(parameter) is None:
			try:
				parameters.pop(parameter)
			except KeyError:
				pass
	
	# auto color
	parameters["color"] = parameters.get("color") or 0x151515
	
	# footer with message info
	if not parameters.get("nofooter") or not parameters.get("footer"):
		now = format_time(discord.utils.utcnow())
		
		# makes sure slash and prefix commands both work
		user = ctx.user if isinstance(ctx, discord.Interaction) else ctx.author
		
		parameters["footer"] = dict(
			text=f"requested by {user.name} at {now}",
			icon_url=user.avatar.url
		)
	
	return Embed.from_dict(parameters)
