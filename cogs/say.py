# have the bot say things in a channel

from discord.ext import commands

class say(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def say(self, ctx, id: int, *words: str):

		if not ctx.author.id == 290983149507182592:
			await ctx.send('You must be me to use that command!')	
	
		try:
			channel = self.bot.get_channel(id)
			await channel.send(' '.join(words))
		except Exception as e:
			await ctx.send(e)
		finally:
			await ct
	
def setup(bot):
	bot.add_cog(say(bot))