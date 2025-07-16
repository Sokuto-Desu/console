import os

from glob import glob
from dotenv import load_dotenv

load_dotenv()

# private tokens
token = os.getenv("TOKEN")
test_token = os.getenv("TEST_TOKEN")

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