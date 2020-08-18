# for deleting all skips of a guild when resetting

from discord.ext import commands, tasks
import discord
import os
import pymongo
import time

class delall(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.messid = {}
		try:
			self.clearActive.start()
		except:
			pass
	
	async def on_ready(self):
		self.clearActive.start()

	def cog_unload(self):
		self.clearActive.stop()

	@commands.command(aliases=['delall'])
	async def reset(self, ctx):
		if not ctx.author == ctx.guild.owner and not discord.utils.get(ctx.guild.roles, name="Trusted") in ctx.author.roles:
			return await ctx.send('You must be the server owner to do that!')

		message = await ctx.send("Are you sure you want to reset all skips?")
		emojis = ['⛔', '✅']
		for emoji in emojis: 
			await message.add_reaction(emoji)
		
		self.messid.update({message.id: time.time()})
    
	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		message = reaction.message
		emoji = reaction.emoji

		if user.bot or user != reaction.message.guild.owner or not message.id in self.messid:
			return

		if emoji == '⛔':
			await message.channel.send('Reset cancelled.')
			del self.messid[message.id]
		
		elif emoji == '✅':
			with pymongo.MongoClient(os.environ.get('MONGO')) as client:
				db = client['skips']
				skips = db['slist']
				query = {
					'guild': message.guild.id
					}
				x = skips.delete_many(query)

				await message.channel.send(f'deleted {x.deleted_count} skips.')
	
			del self.messid[message.id]

	@tasks.loop(seconds=30)
	async def clearActive(self):
		for x in list(self.messid):
			if time.time() - self.messid[x] > 120:
				self.messid.pop(x)
	

def setup(bot):
	bot.add_cog(delall(bot))