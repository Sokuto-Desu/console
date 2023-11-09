from typing import Optional
from utils import reply

from discord import option, Member, slash_command, ApplicationContext, default_permissions
from discord.ext.commands import Cog, has_permissions, MemberConverter, command



class Moderation(
	Cog,
	name="moderation",
	description="moderate your server"
):
	def __init__(self, bot):
		self.bot = bot
	
	
	async def clear_command(self, ctx, amount, user, contains):
		def clear_check(message):
			result = True
			
			if user:
				result = user == message.author
			if contains:
				result = contains in message.content and result
			
			if not ctx.is_app:
				# clearing message of author
				result = result or message == ctx.message 
			
			return result
		
		# 1 is the message of author
		amount = amount + 1 if not ctx.is_app else amount 
		
		cleared = await ctx.channel.purge(limit=amount, check=clear_check)
		cleared_amount = len(cleared) - 1 if not ctx.is_app else len(cleared)
		
		await reply(ctx, f"`successfully cleared {cleared_amount} messages.`", delete_after=1.5)
	
	
	@command(
		aliases=["clear", "purge", "c"],
		description="purge specific amount of messages in channel",
		usage="os.clear r>amount n>user (id or mention) n>contains",
		brief="os.c 50 @Console#3862 // os.c 50 N-word"
	)
	@has_permissions(manage_messages=True)
	async def _clear(self, ctx, amount: int=1, user: Optional[MemberConverter]=None, contains: str=None):
		await self.clear_command(ctx, amount, user, contains)
	
	@slash_command(description="purge specific amount of messages in channel")
	@default_permissions(manage_messages=True)
	@option("amount", description="amount of messages to clear",
			required=True)
	@option("user", description="clear filter: user",
			required=False, default=None)
	@option("contains", description="clear filter: message content",
			required=False, default=None)
	async def clear(self, ctx, amount: int, user: Member, contains: str):
		await self.clear_command(ctx, amount, user, contains)



def setup(bot):
	bot.add_cog(Moderation(bot))