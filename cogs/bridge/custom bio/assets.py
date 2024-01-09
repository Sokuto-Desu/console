import discord

from discord import ButtonStyle, InputTextStyle, Embed
from discord.ui import View, Button, button, Modal, InputText

from db import DetaBase


class EmbedEntry:
	def __init__(
		self,
		name: str,
		input_type: int
	):
		self.label_name = name.capitalize()
		self.name = name
		if input_type == 1:
			self.input_type = InputTextStyle.short
		else:
			self.input_type = InputTextStyle.long


class BioView(View): 
	def __init__(self, user):
		super().__init__()
		
		self.user = user
	
	@button(
		label="Edit",
		style=ButtonStyle.green
	)
	async def callback(self, button, inter):
		if not inter.user.id == self.user.id:
			await inter.response.send_message("That ain't your bio bro", ephemeral=True)
		
		edit_view = EditBioView(self.user)
		
		await inter.response.edit_message(
			embed=inter.message.embeds[0],
			view=edit_view
		)

class EditBioView(View):
	def __init__(self, user):
		super().__init__()
		
		self.user = user
		
		embed_entries =  (
			EmbedEntry("title", 1),
			EmbedEntry("description", 2),
			EmbedEntry("footer", 1),
			EmbedEntry("color", 1),
			EmbedEntry("image", 1),
			EmbedEntry("thumbnail", 1)
		)
		
		for embed_entry in embed_entries:
			self.add_item(
				EditButton(
					user=self.user,
					embed_entry=embed_entry,
#					label=embed_entry.label_name,
#					style=ButtonStyle.blurple
				)
			)
	
	@button(
		label="Finish",
		style=ButtonStyle.red,
		row=3,
		emoji="📍"
	)
	async def finish_callback(self, button, inter):
		if not inter.user.id == self.user.id:
			await inter.response.send_message("That ain't your bio bro", ephemeral=True)
		
		await inter.response.edit_message(embed=inter.message.embeds[0], view=BioView(self.user))

class BioModal(Modal):
	def __init__(
		self, 
		user,
		embed_entry: EmbedEntry,
		*args, 
		**kwargs
	):
		self.embed_entry = embed_entry
		self.db = DetaBase("bio")
		self.user = user
		
		if embed_entry.name in ("image", "thumbnail"):
			title = f"Please input URL for embed's {embed_entry.name}"
		else:
			title = f"Please input embed’s {embed_entry.name}."
		
		super().__init__(title=title, *args, **kwargs)
		
		self.add_item(
			InputText(
				label=embed_entry.label_name, 
				style=embed_entry.input_type
			)
		)
	
	async def callback(self, inter):
		if not inter.user.id == self.user.id:
			await inter.response.send_message("That ain't your bio bro", ephemeral=True)
		
		new_embed = inter.message.embeds[0].to_dict()
		value = self.children[0].value
		
		if self.embed_entry.name == "color":
			value = int(value, 16)
		if self.embed_entry.name == "footer":
			value = {"text": value}
		if self.embed_entry.name in ("image", "thumbnail"):
			value = {"url": value}
		
		new_embed[self.embed_entry.name] = value
		
		self.db.set(
			key=str(inter.user.id),
			value=new_embed
		)
		
		await inter.response.edit_message(
			embed=Embed.from_dict(new_embed), 
			view=EditBioView(self.user)
		)


class EditButton(Button):
	def __init__(
		self,
		user,
		embed_entry: EmbedEntry,
		*args,
		**kwargs
	):
		super().__init__(*args, **kwargs)
		
		self.embed_entry = embed_entry
		self.user = user
		
		self.label = embed_entry.label_name
		self.style = ButtonStyle.blurple
		
		if embed_entry.name in ("color", "image", "thumbnail"):
			self.row = 2
	
	async def callback(self, inter):
		if not inter.user.id == self.user.id:
			await inter.response.send_message("That ain't your bio bro", ephemeral=True)
		
		await inter.response.send_modal(
			BioModal(
				user=self.user,
				embed_entry=self.embed_entry
			)
		)
