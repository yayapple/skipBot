# a command to delete a skip

from discord.ext import commands, tasks
from cogs.default import get_default
from main import get_prefix
import json
import time
import pymongo
import os


class delskip(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.messid = {}


	@commands.command(aliases=['ds', 'd'])
	async def delskip(self, ctx, *args):

		if not ctx.guild:
			return await ctx.send('You can\'t do that here!')
		
		with open('storage/channels.json', 'r') as f:
			channels = json.load(f)
		
		p = get_prefix(ctx, ctx)

		# checks

		if channels.get(str(ctx.guild.id)) is None:
			return await ctx.send(f'Please finish setting up the skip environment first with `{p}help skip`! (Missing whitelist)')

		if get_default(ctx) is None:
			return await ctx.send(f'Please finish setting up the skip environment first with `{p}help skip`! (Missing default)')

		if not ctx.channel.id == channels.get(str(ctx.guild.id)):
			return

		if len(args) != 1:
			await ctx.send('who am i skipping lol')
			return

		name = args[0].lower().replace('\\', '') # format text

		if name == 'skipbot':
			await ctx.send('hey thats me')

		# skip file processing
		with pymongo.MongoClient(os.environ.get('MONGO')) as client:
			db = client['skips']
			skips = db['slist']

			skipData = skips.find_one({
				'name':args[0],
				'guild': ctx.guild.id})
			if skipData is None:
				await ctx.send(f'`{name}` has not skipped yet.')
				return
			else:
				skipsUsed = skipData.get('skips')
				skipAmount = skipData.get('amount')

		#send skip messge

		message = await ctx.send(
				f'`{name}` has used {skipsUsed}/{skipAmount} skips. React ⏪ to undo a skip, react ➖ to allow less.'
				)
		emojis = ['⏪', '➖']

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
		default = get_default(message)

		with pymongo.MongoClient(os.environ.get('MONGO')) as client:
			db = client['skips']
			skips = db['slist']

			skipData = skips.find_one({
				'name': name, 
				'guild': message.guild.id})

		# skip user
		if emoji == '⏪':

			skipsUsed = skipData.get('skips') - 1

			with pymongo.MongoClient(os.environ.get('MONGO')) as client:
				db = client['skips']
				skips = db['slist']
				
				if skipData.get('skips') == 1 and skipData.get('amount') == default:
					skips.delete_one(skipData)
					
				else:
					query = {
						'name': name, 
						'guild': message.guild.id
						}
					skips.update(
						query, 
						{'$set': {'skips': skipsUsed}}
						)

			await message.channel.send(f'Skipped {name}. ({skipsUsed})')
			del self.messid[message.id]
	
			# allow skip	
		elif emoji == '➖':

			skipAmount = skipData.get('amount') - 1
			
			with pymongo.MongoClient(os.environ.get('MONGO')) as client:
				db = client['skips']
				skips = db['slist']

				if skipData.get('skips') == 0 and skipData.get('amount') == default + 1:
					skips.delete_one(skipData)
				
				else:
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
	
	@commands.command(aliases=['sad'])
	async def showActiveDelete(self, ctx):
		if len(self.messid) > 0:
			await ctx.send(self.messid)
		else:
			await ctx.send('No active skip messages')
	
	@tasks.loop(seconds=30)
	async def clearActive(self):
		for x in list(self.messid):
			if time.time() - self.messid[x] > 120:
				self.messid.pop(x)


	@commands.Cog.listener()
	async def on_ready(self):
		self.clearActive.start()


def setup(bot):
	bot.add_cog(delskip(bot))

