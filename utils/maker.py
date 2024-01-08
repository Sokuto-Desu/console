import discord

from discord import Embed

from .misc import format_time

def make_embed(ctx, **parameters) -> Embed:
	# i dont know why i did this but its needed 
	for parameter in ("footer", "title", "description"):
		if parameters.get(parameter) is None:
			try:
				parameters.pop(parameter)
			except KeyError:
				pass
	
	parameters["color"] = parameters.get("color") or 0x151515
	
	if not parameters.get("no_default_footer"):
		now = format_time(discord.utils.utcnow())
		user = ctx.user if isinstance(ctx, discord.Interaction) else ctx.author
		parameters["footer"] = parameters.get("footer") or dict(
			text=f"requested by {user.name} at {now}",
			icon_url=user.avatar.url
		)
	
	return Embed.from_dict(parameters)