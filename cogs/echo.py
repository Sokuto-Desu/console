import discord
from discord import slash_command
from discord.ext import commands

from ast import literal_eval


class Echo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.echo_docs = """
**content**: message content. `|` length: from 1 to 2000.

=================

**title**: embed title `|` length: from 1 to 256.
**description**: embed description `|` length: from 1 to 4000.
**footer**: embed footer `|` length: from 1 to 2048.

**fields**: embed fields. name/value `|` length: name - from 1 to 256, value - from 1 to 1024.
**fields usage**: ```
-add field name // field value -add field name // field value ...```

**color**: embed color `|` uses: 0x code.
**color examples**: `0x219392`, `0xF281B3`
0x000000 - no color.

**image**: embed image. `|` uses: any image url.
**thumbnail**: embed thumbnail. `|` uses: any image url.

**id**: id of message sent by Console. use this if you need to edit an already existing message. only for administrators.

=================

**echo usage example**: `/echo content:message content title:embed title description:embed description footer:embed footer fields:-add field // value image:[url] thumbnail:[url] buttons:see below`
**echo examples**: [click me](https://cdn.discordapp.com/attachments/954469674983256124/1003628978466209822/IMG_20220801_140532.jpg) `|` [click me](https://cdn.discordapp.com/attachments/954469674983256124/1003628978856271893/IMG_20220801_140540.jpg)

=================

**buttons**: message buttons.

**buttons usage**: ```
{"label": "button label (text)", 
"style": "button style (see below; default is primary)", 
"emoji": "button emoji (unicode emoji; you can skip this if you don't want the emoji in the button)",
"disabled": "is button disabled (true/false; you can skip this if you need an enabled button)"
"url": "use this if button style is "link" (url)", 
"callback": "text that will be displayed after someone presses button (you can skip this if you don't need a callback)", 
"ephemeral": "ephemeral callback message (true/false; you can skip this if you need an ephemeral callback message)"}; {button 2}; {button 3}; ...```

[button styles](https://cdn.discordapp.com/attachments/954469674983256124/1003631816659456071/IMG_20220801_145427.jpg): 
```
primary `/` blurple
secondary `/` grey
success `/` green
danger `/` red
link `/` url``` 
you can use any name provided here.

[button example](https://cdn.discordapp.com/attachments/954469674983256124/1003633188268163213/IMG_20220801_145944.jpg): ```
{"label": "click me", "style": "green", "disabled": "false", "callback": "Hello world!", "ephemeral": "true"}```
**note**: you can use ' instead of "
"""
	
	
	class EchoButton(discord.ui.Button):
		def __init__(self, label, style, callback_text, ephemeral, emoji, disabled, url=None):
			style = getattr(discord.ButtonStyle, style)
			super().__init__(
			label = label,
				style = style,
				emoji = emoji,
				disabled = disabled,
				url = url if style == discord.ButtonStyle.link else None
			)
			
			self.disabled = disabled
			self.callback_text = callback_text
			self.ephemeral = ephemeral
		
		
		async def callback(self, inter):
			if not self.callback_text or self.disabled:
				return
			await inter.response.send_message(content = self.callback_text, ephemeral = self.ephemeral)
	
	
	def converttobuttons(self, buttons: str):
		styles = ["primary", "blurple", "secondary", "grey", "success", "green", "danger", "red", "link", "url"]
		
		buttons_list = buttons.split(";")
		
		class NewView(discord.ui.View):
			def __init__(self):
				super().__init__(timeout = None)
		
		view = NewView()
		
		
		for button in buttons_list:
			
			button_dict = literal_eval(button)
			
			label = button_dict.get("label")
			if not label:
				label = "ᅠ"
			
			style = button_dict.get("style")
			if not style or style not in styles:
				style = "primary"
			
			ephemeral = button_dict.get("ephemeral")
			if ephemeral == "true" or not ephemeral:
				ephemeral = True
			else:
				ephemeral = False
			
			disabled = button_dict.get("disabled")
			if not disabled or disabled != "true":
				disabled = False
			else:
				disabled = True
			
			button_item = EchoButton(label, style, button_dict.get("callback"), ephemeral, button_dict.get("emoji"), disabled, button_dict.get("url"))
			
			view.add_item(button_item)
		
		return view
	
	
	
	@slash_command(description="echo (/embed replacement). os.echo for more info.")
	@discord.default_permissions(manage_messages = True)
	async def echo(
		self,
		ctx,
		content: Option(str, "any text", required=False, default=None),
		title: Option(str, "title of embed", required=False, default=""), 
		description: Option(str, "description of embed", required=False, default=""),
		footer: Option(str, "footer of embed", required=False, default=Embed.Empty),
		fields: Option(str, "-add field // value -add field // value", required=False, default=None),
		color: Option(str, "color of embed", required=False, default=None),
		image: Option(str, "image url of embed", required=False, default=None),
		thumbnail: Option(str, "thumbnail url of embed", required=False, default=None),
		buttons: Option(str, 'message buttons. check "info" parameter for more info.', required=False, default=None),
		id: Option(str, "id of message sent by Console. use this if you need to edit an already existing embed.", required=False, default=None),
		info: Option(bool, "display echo info?", required=False, default = False)
		):
		
		if info:
			embed = discord.Embed(
				title = "echo command info.",
				description = self.echo_docs,
				color = 0x151515
				)
			
			await ctx.delete()
			return await ctx.channel.send(embed = embed)
		
		emb = Embed(title=title, description=description).set_footer(text=footer)
		emb.set_image(url=image) if image != None else None
		emb.set_thumbnail(url=thumbnail) if thumbnail != None else None
		
		try:
			fields = fields.split("-add")[1:]
			for f in fields:
				f = f.split("//")
				emb.add_field(name=f[0], value=f[1])
		except:
			pass
		
		if emb:
			emb.color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) if color == None else int(color, 16)
		else:
			emb = None
		
		view = None
		if buttons:
			try:
				view = converttobuttons(buttons)
			except Exception as e:
				raise e
		
		if id != None:
			if ctx.author.guild_permissions.administrator:
				try:
					msge = await ctx.channel.fetch_message(int(id))
					await msge.edit(embed=emb)
					await ctx.respond("`embed succesfully edited.`", ephemeral=True)
				except:
					await ctx.respond("`can't found message. check if this message exists in current channel.`", ephemeral=True)
			else:
				await ctx.send("`you don't have 'Administrator' permission to edit the embed.`", ephemeral=True)
			return
		
		await ctx.delete()
		await ctx.channel.send(content = content, embed = emb, view = view)



def setup(bot):
	bot.add_cog(Echo(bot))