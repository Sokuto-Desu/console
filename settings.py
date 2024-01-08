import discord
import os

from discord.ext import commands
from discord.ext.bridge import Bot

from sys import argv
from glob import iglob
from dotenv import load_dotenv

from db import DetaBase

"""
TODO:
Restructurization for utils/ and cogs/
"""

settings_db = DetaBase("settings")
load_dotenv()

token = os.getenv("TOKEN")
test_token = os.getenv("TEST_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

owners = list(map(
	lambda id: int(id),
	settings_db.get("owners") or [898610134589243442]
))
errors_channel = int(settings_db.get("errors_channel")) or 989094089305772042
devserver = int(settings_db.get("devserver")) or 942390181984608327

activity = discord.Activity(
	type = discord.ActivityType.watching,
	name = settings_db.get("activity") or "/help"
)

test_mode = False if not "-t" in argv else True
default_prefix = "os."


async def get_guild_prefix(bot: Bot | None, message):
	if test_mode:
		return "sudo." 
	
	prefixes_db = DetaBase("prefixes")
	
	guild_id = str(message.guild.id)
	
	guild_prefix = prefixes_db.get(guild_id, set_default=default_prefix)
	
	return guild_prefix


bridge_cogs = [
	file_path.replace(os.path.sep, ".")[:-3]
	for file_path in iglob("cogs/bridge/**/*.py", recursive=True)
	if not file_path.endswith("assets.py")
]

slash_cogs = [
	file_path.replace(os.path.sep, ".")[:-3]
	for file_path in iglob("cogs/slash/**/*.py", recursive=True)
	if not file_path.endswith("assets.py")
]



echo_info = """
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
"emoji": "button emoji (unicode emoji); you can skip this if you don't want the emoji in the button)",
"disabled": "is button disabled (true/false); you can skip this if you need an enabled button)"
"url": "use this if button style is "link" (url)", 
"callback": "text that will be displayed after someone presses button (you can skip this if you don't need a callback)", 
"ephemeral": "ephemeral callback message (true/false; you can skip this if you need an ephemeral callback message)"}; {button 2}; {button 3}; ...```

[button styles](https://cdn.discordapp.com/attachments/954469674983256124/1003631816659456071/IMG_20220801_145427.jpg): 
```
primary / blurple
secondary / grey
success / green
danger / red
link / url``` 
you can use any name provided here.

[button example](https://cdn.discordapp.com/attachments/954469674983256124/1003633188268163213/IMG_20220801_145944.jpg): ```
{"label": "click me", "style": "green", "disabled": "false", "callback": "Hello world!", "ephemeral": "true"}```
**note**: you can use ' instead of "
"""
