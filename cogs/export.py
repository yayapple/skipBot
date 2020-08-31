# command to backup the skips into a local file

import pymongo
import os
from discord.ext import commands
import discord

	
			

class export(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
	
	
	@commands.command(aliases=['backup'])
	@commands.has_permissions(administrator=True)
	async def export(self, ctx):
		with pymongo.MongoClient(os.environ.get('MONGO')) as client:
			db = client['skips']
			skips = db['slist']
			cursor = list(skips.find({'guild': ctx.guild.id}))

			if not cursor:
				await ctx.send("There are no skips to export!")
				return
			for document in cursor:
				with open(f'{ctx.guild.id}.txt', 'a+') as f:
					f.write(f'{document.get("name")} {document.get("skips")}/{document.get("amount")}\n')
					
		with open(f'{ctx.guild.id}.txt', 'rb') as fp:
			await ctx.send(file=discord.File(fp, 'Skips.txt'))
		
		os.remove(f'{ctx.guild.id}.txt')

	@export.error
	async def permsError(ctx, error):	
		if isinstance(error, commands.MissingPermissions):
			await ctx.send('You must be an administrator to use that command.')
		

def setup(bot):
	bot.add_cog(export(bot))