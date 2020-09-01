# misc commands unrelated to skipping.

import discord
import pymongo
import os
from discord.ext import commands
from main import get_prefix, updateDict, addEntry

class misc(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# register command (temp)

	@commands.command()
	async def register(self, ctx):

		addEntry(ctx.guild)

		with pymongo.MongoClient(os.environ.get('MONGO')) as client:
			db = client['skips']
			config = db['guild config']

			entry = config.find_one({'guild': ctx.guild.id})

			if entry:
				return await ctx.send('already registered')
			else:
				config.insert_one({
					'guild': ctx.guild.id,
					'prefix': '?',
					'default': '',
					'channel': ''
				})
				await ctx.send('registered')

	# prefix command

	@commands.command(aliases=['skipPrefix'])
	@commands.has_permissions(administrator=True)
	async def prefix(self, ctx, *prefix):

		if len(prefix) != 1:
			return await ctx.send('Please enter a valid prefix.')

		updateDict(ctx, 'prefix', prefix[0])

		with pymongo.MongoClient(os.environ.get('MONGO')) as client:
			db = client['skips']
			config = db['guild config']

			config.update(
				{'guild': ctx.guild.id},
				{'$set': {'prefix': prefix[0]}}
			)
		
		await ctx.send(f'changed prefix to "{prefix[0]}"')

	@prefix.error
	async def permsError(self, ctx, error):	
		if isinstance(error, commands.MissingPermissions):
			await ctx.send('You must be an administrator to use that command.')

	# invite command

	@commands.command()
	async def invite(self, ctx):
		embed = discord.Embed(
			title = "Invite link", 
			color = discord.Color.gold(),
			description = '[Click here to invite the bot](https://discord.com/oauth2/authorize?client_id=711998861165592728&permissions=8&scope=bot)')
		await ctx.send(embed=embed)
	

	# ping command

	@commands.command()
	async def ping(self, ctx):
		ping = int(self.bot.latency * 1000)
		embed = discord.Embed(
			title = "Pong", 
			color = discord.Color.gold(),
			description = f"{ping}ms")
		await ctx.send(embed=embed)
	
def setup(bot):
	bot.add_cog(misc(bot))
