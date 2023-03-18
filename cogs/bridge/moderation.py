import openai

from typing import Optional

from discord import option, Member
from discord.ext.commands import Cog, has_permissions, MemberConverter, command
from discord.ext.bridge import bridge_command

openai.api_key = "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"

class Moderation(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	
	@bridge_command(aliases=["c", "purge"], help="purge specific amount of messages in channel", usage="os.clear >amount -user (id or mention) -contains")
	@has_permissions(manage_messages = True)
	@option("amount", int, description="amount of messages to clear", required=True)
	@option("user", Member, description="clear filter: user", required=False, default=None)
	@option("contains", str, description="clear filter: message content", required=False, default=None)
	async def clear(self, ctx, amount: int = 1, user: Optional[MemberConverter] = None, contains: str = None):
		def clear_check(message):
			result = True
			
			if user:
				result = user == message.author
			if contains:
				result = contains in message.content and result
			
			return result or message == ctx.message 
		
		
		cleared = await ctx.channel.purge(limit=amount + 1, check=clear_check)
		
		await ctx.send(f"`successfully cleared {len(cleared) - 1} messages!`", delete_after=1.5)
	
	@command()
	async def chat(self, ctx, *, prompt):
		message = await ctx.send("`please wait a minute.`")
		
		result = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
		
		await message.edit(f"`please wait a minute.`\n```\n{result.choices[0].message.content}```")



def setup(bot):
	bot.add_cog(Moderation(bot))