# whitelist command to set skip channel

from discord.ext import commands
import json

class whitelist(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	# whitelist command

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def whitelist(self, ctx):
		with open('storage/channels.json', 'r') as f:
			channels = json.load(f)

		channels[str(ctx.guild.id)] = ctx.channel.id

		with open('storage/channels.json', 'w') as f:
			json.dump(channels, f, indent = 2)

		await ctx.send(f'Changed the whitelisted channel to {str(ctx.channel)}.')

	@whitelist.error
	async def permsError(self, ctx, error):	
		if isinstance(error, commands.MissingPermissions):
			await ctx.send('You must be an administrator to use that command.')


def setup(bot):
	bot.add_cog(whitelist(bot))

