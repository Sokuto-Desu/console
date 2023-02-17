import settings
import discord


async def close(message: discord.Message, time: int = 5):
	await asyncio.sleep(time)
	await message.delete()

# converts time (8m, 1h, 2d, etc.) to seconds
async def convert_time(time):
	time_list = re.split('(\d+)', time)
	if time_list[2] == "s":
		times = int(time_list[1])
	if time_list[2] == "m":
		times = int(time_list[1]) * 60
	if time_list[2] == "h":
		times = int(time_list[1]) * 60 * 60
	if time_list[2] == "d":
		times = int(time_list[1]) * 60 * 60 * 24
	
	return times


class Embed(discord.Embed):
	@staticmethod
	def create(**parameters):
		if not parameters.get("color"):
			parameters["color"] = 0x151515
		
		# setdefault() but returns dictionary
		def default(dictionary, key, value):
			dictionary.setdefault(key, value)
			return dictionary
		
		if fields := parameters.get("fields"):
			parameters["fields"] = [
				default(field, "inline", False)
				for field in fields
			]
		
		for parameter in ("image", "thumbnail", "footer", "title", "description"):
			if parameters.get(parameter) in (None, Embed.Empty):
				parameters.pop(parameter)
		
		return discord.Embed.from_dict(parameters)