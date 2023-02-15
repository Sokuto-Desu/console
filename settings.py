from dotenv import load_dotenv
import os

load_dotenv()

config = {
#	"prefix": ["os.", "cmd.", "Os.", "Cmd.", "OS.", "CMd.", "CMD."],
 	"owners": [898610134589243442],
 	"devserver": [922482556224548975, 942390181984608327],
 	"activity": "/help",
 	"token": os.getenv("TOKEN"),
 	"test_token": os.getenv("TEST_TOKEN"),
	"is_test": True,
 	"errors_channel": 989094089305772042
}

cogs = [
	f"cogs.{file_name[:-3]}"
	for file_name in os.listdir("./cogs")
	if file_name[-3:] == ".py"
	]