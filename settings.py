from dotenv import load_dotenv
from os import getenv, listdir

load_dotenv()

prefix = ["os.", "cmd.", "Os.", "Cmd.", "OS.", "CMd.", "CMD."]
owners = [898610134589243442]
devserver = 942390181984608327
activity = "/help"
token = getenv("TOKEN")
test_token = getenv("TEST_TOKEN")

is_test = False
errors_channel = 989094089305772042
deta_key = getenv("deta_key")


cogs = [
	f"cogs.bridge.{file_name[:-3]}"
	for file_name in listdir("./cogs/bridge")
	if file_name[-3:] == ".py"
]
cogs_slash = [
	f"cogs.slash.{file_name[:-3]}"
	for file_name in listdir("./cogs/slash")
	if file_name[-3:] == ".py"
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