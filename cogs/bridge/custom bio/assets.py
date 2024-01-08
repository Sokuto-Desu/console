import discord

from discord import ButtonStyle, InputTextStyle, Embed
from discord.ui import View, Button, button, Modal, InputText

from db import DetaBase


class BioView(View):
	@button(
		label="Edit",
		style=ButtonStyle.green
	)
	async def callback(self, button, inter):
		edit_view = EditBioView()
		await inter.response.edit_message(
			embed=inter.message.embeds[0],
			view=edit_view
		)

class EditBioView(View):
	def __init__(self):
		super().__init__()
		
		embed_attrs =  (
			("Title", 1), 
			("Description", 2), 
			("Footer", 1), 
			("Color", 1)
		)
		
		for item, input_type in embed_attrs:
			self.add_item(
				EditButton(
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
		await inter.response.edit_message(embed=inter.message.embeds[0], view=BioView())

class BioModal(Modal):
	def __init__(
		self, 
		input_name: str="Title", 
		embed_entry: str="title", 
		input_type: int=1, 
		*args, 
		**kwargs
	):
		super().__init__(*args, **kwargs)
		
		self.embed_entry = embed_entry
		self.db = DetaBase("bio")
		
		if input_type == 1:
			self.add_item(InputText(label=input_name))
		elif input_type == 2:
			self.add_item(InputText(label=input_name, style=InputTextStyle.long))
	
	async def callback(self, inter):
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
		
		await inter.response.edit_message(embed=Embed.from_dict(new_embed), view=EditBioView())


class EditButton(Button):
	def __init__(
		self,
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
	
	async def callback(self, inter):
		await inter.response.send_modal(
			BioModal(
				input_name=self.input_name,
				embed_entry=self.embed_entry,
				input_type=self.input_type,
				title=f"Please input embed’s {self.input_name}."
			)
		)