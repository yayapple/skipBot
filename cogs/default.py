# a command to set the default amount of skips in a server.

import pymongo
import os
from discord.ext import commands
from main import updateDict	
import discord

class default(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	

	@commands.command(aliases=['default'])
	async def setdefault(self, ctx, *args):

		if not ctx.author == ctx.guild.owner and not discord.utils.get(ctx.guild.roles, name="Trusted") in ctx.author.roles:
			return await ctx.send('You must be the server owner to do that!')

		elif len(args) != 1 or not args[0].isdigit():
			return await ctx.send('Please enter a valid number!')

		updateDict(ctx, 'default', int(args[0]))
	
		with pymongo.MongoClient(os.environ.get('MONGO')) as client:
			db = client['skips']
			config = db['guild config']

			config.update(
				{'guild': ctx.guild.id},
				{'$set': {'default': int(args[0])}}
			)

		await ctx.send(f'Set default skip amount to {args[0]}. Any skip entries before now will still have the prevous skip amount.')




def setup(bot):
	bot.add_cog(default(bot))