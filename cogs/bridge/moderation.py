from typing import Optional

from discord import option, Member
from discord.ext.commands import Cog, has_permissions, MemberConverter
from discord.ext.bridge import bridge_command


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



def setup(bot):
	bot.add_cog(Moderation(bot))