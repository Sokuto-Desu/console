from utils import make_embed, make_buttons
from ast import literal_eval
from random import randint

from discord import slash_command, option, ButtonStyle, Permissions, Colour
from discord.ext.commands import Cog, MissingPermissions, MessageNotFound
from discord.ui import View


class Echo(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	
	@slash_command(description="echo (/embed replacement). /info echo for more info")
	@option("content", description="any text",
			required=False, default=None)
	@option("title", description="any text",
			required=False, default=None)
	@option("description", description="description of embed",
			required=False, default=None)
	@option("footer", description="footer of embed",
			required=False, default=None)
	@option("color", description="color of embed (hex, e.g. 0x151515)",
			required=False, default=None)
	@option("fields", description="-add field name // value -add field name // value",
			required=False, default=None)
	@option("image", description="url of embeds image",
			required=False, default=None)
	@option("thumbnail", description="url of embeds thumbnail",
			required=False, default=None)
	@option("buttons", description="message buttons. check",
			required=False, default=None)
	@option("id", description="id of message sent by Console. use this to edit existing message.",
			required=False, default=None)
	async def echo(self, ctx, content: str,
					title: str, description: str, footer: str,
					color: str, fields: str, image: str,
					thumbnail: str, buttons: str, id: str):
		
		
		fields_list = []
		if fields:
			fields = fields.split("-add")[1:] # [1:] to remove empty string
			for field in fields:
				field = field.split("//") # splits to [name, value]
				fields_list.append(
					{"name": field[0],
					"value": field[1]})
		
		
		if not any((title, description, footer, image, thumbnail, fields)):
			embed = None
		else:
			color = int(color, 16) if color else Colour.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255))
			
			embed = make_embed(
				title=title,
				description=description,
				color=color,
				footer={"text": footer},
				image={"url": image},
				thumbnail={"url": thumbnail},
				fields=fields_list
			)
		
		
		if id:
			if not ctx.author.guild_permissions.manage_messages:
				raise MissingPermissions(["manage_messages"])
			else:
				try:
					message = await ctx.channel.fetch_message(int(id))
					await message.edit(content=content, embed=embed)
					
					await ctx.respond("`embed succesfully edited.`", ephemeral=True)
				except MessageNotFound:
					await ctx.respond("`can't found message. check if this message exists in current channel.`", ephemeral=True)
			return
		
		view = None
		if buttons:
			buttons = buttons.split(";")
			buttons = literal_eval(buttons)
			
			view = View()
			view.add_item(make_buttons(buttons))
		
		await ctx.delete()
		await ctx.send(content=content, embed=embed, view=view)



def setup(bot):
	bot.add_cog(Echo(bot))