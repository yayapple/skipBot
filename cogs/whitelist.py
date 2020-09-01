# whitelist command to set skip channel

from discord.ext import commands
from main import updateDict
import os
import pymongo

class whitelist(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	# whitelist command

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def whitelist(self, ctx):

		updateDict(ctx, 'channel', ctx.channel.id)

		with pymongo.MongoClient(os.environ.get('MONGO')) as client:
			db = client['skips']
			config = db['guild config']

			config.update(
				{'guild': ctx.guild.id},
				{'$set': {'channel': ctx.channel.id}}
			)

		await ctx.send(f'Changed the whitelisted channel to {str(ctx.channel)}.')

	@whitelist.error
	async def permsError(self, ctx, error):	
		if isinstance(error, commands.MissingPermissions):
			await ctx.send('You must be an administrator to use that command.')


def setup(bot):
	bot.add_cog(whitelist(bot))

