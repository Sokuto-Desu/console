import discord

from typing import Union

from discord import Embed, ButtonStyle, PartialEmoji
from discord.ui import View, Button

from .misc import format_time


class CustomButton(Button):
	def __init__(self, label: str, style: str, callback: Union[dict, str], ephemeral: bool, disabled: bool, emoji: PartialEmoji, url: str=None):
		"""Button with custom callback
		label: str 
			any text
		style: str 
			primary, secondary, success, danger or aliases
		callback: dict or str 
			if str, argument will be used as a callback respond content
			if dict, you should pass arguments for discord.abc.Messageable.send
		ephemeral: bool
		disabled: bool
		emoji: discord.PartialEmoji
		url: str
		"""
		
		style = getattr(ButtonStyle, style)
		
		super().__init__(
			label=label,
			style=style,
			emoji=emoji,
			disabled=disabled,
			url=url if style == ButtonStyle.link else None
		)
		
		self.disabled = disabled
		self.ephemeral = ephemeral
		self.callback_arg = callback
	
	
	async def callback(self, interaction):
		if not self.callback_arg or self.disabled:
			return
		
		if isinstance(self.callback_arg, str):
			await interaction.response.send_message(content=self.callback_arg, ephemeral=self.ephemeral)
		else:
			await interaction.response.send_message(**self.callback_arg)


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


def make_buttons(buttons_list: list) -> list:
	items = []
	
	for button_dict in buttons_list:
		label = button_dict.get("label") or "ᅠ"
		style = button_dict.get("style") or "primary"
		ephemeral = False if button_dict.get("ephemeral") == "false" else True
		disabled = True if button_dict.get("disabled") == "true" else False
		callback = button_dict.get("callback")
		emoji = button_dict.get("emoji")
		url = button_dict.get("url")
		
		button_item = CustomButton(
			label=label,
			style=style,
			callback=callback,
			ephemeral=ephemeral,
			emoji=emoji,
			disabled=disabled,
			url=url
		)
		
		items.append(button_item)
	
	return items