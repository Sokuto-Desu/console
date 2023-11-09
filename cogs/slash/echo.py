from utils import make_embed, make_buttons
from ast import literal_eval
from random import randint

from discord import slash_command, option, ButtonStyle, Permissions, Colour
from discord.ext.commands import Cog, MissingPermissions, MessageNotFound
from discord.ui import View


class Echo(
	Cog,
	name="echo",
	description="/echo command. see /info echo for full info."
):
	def __init__(self, bot):
		self.bot = bot
	
	
	# sorry for this one hell of "required=False, default=None"
	@slash_command(description='say something as a bot. includes embed. "/info echo" for more info')
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
	@option("buttons", description='message buttons. check "/info echo" for more info.',
			required=False, default=None)
	@option("id", description="id of message sent by Console. use this to edit existing message.",
			required=False, default=None)
	async def echo(self, ctx, content: str,
					title: str, description: str, footer: str,
					color: str, fields: str, image: str,
					thumbnail: str, buttons: str, id: str):
		
		fields_list = []
		if fields:
			# [1:] to remove empty string
			fields = fields.split("-add")[1:] 
			for field in fields:
				# splits to [name, value]
				field = field.split("//") 
				fields_list.append(
					{
						"name": field[0],
						"value": field[1],
						"inline": False
					}
				)
		
		
		if not any((title, description, footer, image, thumbnail, fields)):
			embed = None
		else:
			if not color:
				color = Colour.from_rgb(
					randint(0, 255), 
					randint(0, 255), 
					randint(0, 255)
				).value
			else:
				color = int(color, 16) 
			
			embed = make_embed(
				ctx,
				title=title,
				description=description,
				color=color,
				footer=dict(text=footer),
				no_default_footer=True,
				image=dict(url=image),
				thumbnail=dict(url=image),
				fields=fields_list
			)
		
		
		if id:
			if not ctx.author.guild_permissions.manage_messages:
				raise MissingPermissions(["manage_messages"])
			
			try:
				message = await ctx.channel.fetch_message(int(id))
				await message.edit(content=content, embed=embed)
				
				await ctx.respond("`message succesfully edited.`", ephemeral=True)
			except MessageNotFound:
				await ctx.respond("`can't found message. check if this message exists in current channel.`", ephemeral=True)
			finally:
				return
		
		view = None
		if buttons:
			buttons = buttons.split(";")
			buttons_list = []
			for button in buttons:
				# literal_eval is "{}" to {}
				buttons_list.append(literal_eval(button)) 
			
			view = View()
			for button in make_buttons(buttons_list):
				view.add_item(button)
		
		#await ctx.respond("ᅠ", delete_after=0)
		await ctx.delete()
		await ctx.send(content=content, embed=embed, view=view)



def setup(bot):
	bot.add_cog(Echo(bot))