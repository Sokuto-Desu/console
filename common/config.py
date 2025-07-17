import os, discord

from glob import glob
from sys import argv
from dotenv import load_dotenv

load_dotenv()

# private tokens
token = os.getenv("TOKEN")
test_token = os.getenv("TEST_TOKEN")

# main data
activity = discord.Activity(
	type = discord.ActivityType.watching,
	name = "os.help"
)

test_mode = False if "-t" not in argv else True
default_prefix = "os."

developer_server = 1288619328123699232

async def get_guild_prefix(bot, message):
	# temporary
	return default_prefix

# lists cogs (e.g. "cogs.bridge.utility.utility")
def get_cogs():
	# finds cog folders
	cog_folders = glob("cogs/bridge/*/") + glob("cogs/slash/*/")
	
	cogs = []
	for folder in cog_folders:
		# finds the last folder name (e.g. "echo")
		folder_name = os.path.basename(os.path.normpath(folder))
		
		# "echo/" -> "echo/echo"
		file_path = os.path.join(folder, folder_name)
		
		# / -> . (needed for cogs idk why)
		cogs.append(file_path.replace("/", "."))
	
	return cogs