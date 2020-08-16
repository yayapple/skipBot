# commands including or related to the skip command.

from discord.ext import commands, tasks
from cogs.default import get_default
from main import get_prefix
import json
import time
import pymongo
import os


class skip(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.messid = {}
		self.clearActive.start()


	@commands.command(aliases=['s'])
	async def skip(self, ctx, *args):

		if not ctx.guild:
			return await ctx.send('You can\'t do that here!')

		p = get_prefix(ctx,ctx)		

		with open('storage/channels.json', 'r') as f:
			channels = json.load(f)
		
		# checks

		if channels.get(str(ctx.guild.id)) is None:
			return await ctx.send(f'Please finish setting up the skip environment first with `{p}help skip`! (Missing whitelist)')

		elif get_default(ctx) is None:
			return await ctx.send(f'Please finish setting up the skip environment first with `{p}help skip`! (Missing default)')

		elif not ctx.channel.id == channels.get(str(ctx.guild.id)):
			return

		elif len(args) != 1:
			return await ctx.send('Please enter a valid username.')
	
		elif args[0].lower == 'skipbot':
			await ctx.send('hey thats me')

		name = args[0].lower().replace('\\', '') # format text
		defaultSkips = get_default(ctx)
		

		# skip file processing
		with pymongo.MongoClient(os.environ.get('MONGO')) as client:
			db = client['skips']
			skips = db['slist']

			skipData = skips.find_one({
				'name': name,
				'guild': ctx.guild.id})
			if skipData is None:
				skipsUsed = 0
				skipAmount = defaultSkips
			else:
				skipsUsed = skipData.get('skips')
				skipAmount = skipData.get('amount')

		if skipsUsed >= skipAmount:
			message = await ctx.send(f'`{name}` has used all of their skips. React ➕ to add more.')
			emojis = ['➕']

		#send skip messge
		else:
			message = await ctx.send(
					f'`{name}` has used {skipsUsed}/{skipAmount} skips. React ⏩ to skip, react ➕ to allow more.'
					)
			emojis = ['⏩', '➕']

		for emoji in emojis: 
			await message.add_reaction(emoji)
		
		self.messid.update({message.id: time.time()})

	# get reactions (skip command part 2)
	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		message = reaction.message
		emoji = reaction.emoji

		if user.bot or not message.id in self.messid:
			return

		name = message.content.split(' ')[0][1:-1]
		defaultSkips = get_default(message)

		with pymongo.MongoClient(os.environ.get('MONGO')) as client:
			db = client['skips']
			skips = db['slist']

			skipData = skips.find_one({
				'name': name, 
				'guild': message.guild.id})
			print(skipData) # debug


		# skip user
		if emoji == '⏩':
			if skipData is None:
				skipsUsed = 1

				with pymongo.MongoClient(os.environ.get('MONGO')) as client:
					db = client['skips']
					skips = db['slist']
					skips.insert_one({
						'name': name, 
						'skips': 1, 
						'amount': defaultSkips,
						'guild': message.guild.id
						})
			else:
				skipsUsed = skipData.get('skips') + 1

				with pymongo.MongoClient(os.environ.get('MONGO')) as client:
					db = client['skips']
					skips = db['slist']
					query = {
						'name': name, 
						'guild': message.guild.id
						}

					skips.update(
						query, 
						{'$set': {'skips': skipsUsed}}
						)
				
			await message.channel.send(f'Skipped `{name}`. ({skipsUsed})')
			del self.messid[message.id]
		
			# allow skip	
		elif emoji == "➕":
			if skipData is None:
				skipAmount = defaultSkips + 1

				with pymongo.MongoClient(os.environ.get('MONGO')) as client:
					db = client['skips']
					skips = db['slist']
					skips.insert_one({
						'name': name, 
						'skips': 0, 
						'amount': skipAmount,
						'guild': message.guild.id
						})
			else:
				skipAmount = skipData.get('amount') + 1
				
				with pymongo.MongoClient(os.environ.get('MONGO')) as client:
					db = client['skips']
					skips = db['slist']
					query = {
						'name': name, 
						'guild': message.guild.id
						}
					
					skips.update(
						query, 
						{'$set': {'amount': skipAmount}}
						)

			await message.channel.send(f'Allowed {skipAmount} skips for `{name}`.')
			del self.messid[message.id]
		return
	
	@commands.command(aliases=['sa'])
	async def showActive(self, ctx):
		if len(self.messid) > 0:
			await ctx.send(self.messid)
		else:
			await ctx.send('No active skip messages')
	
	@tasks.loop(seconds=30)
	async def clearActive(self):
		for x in list(self.messid):
			if time.time() - self.messid[x] > 120:
				self.messid.pop(x)
		

def setup(bot):
	bot.add_cog(skip(bot))