import discord

from discord import ButtonStyle, InputTextStyle, Embed
from discord.ui import View, Button, button, Modal, InputText

from db import DetaBase


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
		
		embed_attrs =  (
			("Title", 1), 
			("Description", 2), 
			("Footer", 1), 
			("Color", 1)
		)
		
		for item, input_type in embed_attrs:
			self.add_item(
				EditButton(
					user=self.user,
					input_name=item,
					embed_entry=item.lower(),
					input_type=input_type,
					label=item,
					style=ButtonStyle.blurple
				)
			)
	
	@button(
		label="Finish",
		style=ButtonStyle.red
	)
	async def finish_callback(self, button, inter):
		if not inter.user.id == self.user.id:
			await inter.response.send_message("That ain't your bio bro", ephemeral=True)
		
		await inter.response.edit_message(embed=inter.message.embeds[0], view=BioView(self.user))

class BioModal(Modal):
	def __init__(
		self, 
		user,
		input_name: str="Title", 
		embed_entry: str="title", 
		input_type: int=1, 
		*args, 
		**kwargs
	):
		super().__init__(*args, **kwargs)
		
		self.embed_entry = embed_entry
		self.db = DetaBase("bio")
		self.user = user
		
		if input_type == 1:
			self.add_item(InputText(label=input_name))
		elif input_type == 2:
			self.add_item(InputText(label=input_name, style=InputTextStyle.long))
	
	async def callback(self, inter):
		if not inter.user.id == self.user.id:
			await inter.response.send_message("That ain't your bio bro", ephemeral=True)
		
		new_embed = inter.message.embeds[0].to_dict()
		value = self.children[0].value
		
		if self.embed_entry == "color":
			value = int(value, 16)
		if self.embed_entry == "footer":
			value = {"text": value}
		
		
		new_embed[self.embed_entry] = value
		
		self.db.set(
			key=str(inter.user.id), 
			value=new_embed
		)
		
		await inter.response.edit_message(embed=Embed.from_dict(new_embed), view=EditBioView(self.user))


class EditButton(Button):
	def __init__(
		self,
		user,
		input_name: str="Title",
		embed_entry: str="title", 
		input_type: int=1,
		*args,
		**kwargs
	):
		super().__init__(*args, **kwargs)
		
		self.input_name = input_name
		self.embed_entry = embed_entry
		self.input_type = input_type
		self.user = user
	
	async def callback(self, inter):
		if not inter.user.id == self.user.id:
			await inter.response.send_message("That ain't your bio bro", ephemeral=True)
		
		await inter.response.send_modal(
			BioModal(
				user=self.user,
				input_name=self.input_name,
				embed_entry=self.embed_entry,
				input_type=self.input_type,
				title=f"Please input embed’s {self.input_name}."
			)
		)