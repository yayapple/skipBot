
# to do:

# tell that it will reset current skips and replace them with imported skips

import discord
import pymongo
import re
import os
from discord.ext import commands
from requests import get


class simport(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	@commands.command(aliases=['import'])
	async def im(self, ctx):
		file = ctx.message.attachments
		if file == []:
			await ctx.send('Please attach a file with the command.')
			return
		
		elif not ctx.author == ctx.guild.owner and not discord.utils.get(ctx.guild.roles, name="Trusted") in ctx.author.roles:
			return await ctx.send('You must be the server owner to do that!')

		url = file[0].url
		lines = get(url).text.split('\n')
		
		sample = re.split(' |/', lines[0])

		if not type(sample[0]) == str or not sample[1].isdigit() or not sample[2].isdigit():
			return await ctx.send('File is not formatted correctly.')
			
		message = await ctx.send(f'Started importing skips.')
		
		skiplist = []

		err = 0

		for line in lines:
			entry = re.split(' |/', line)
			if line == '':
				continue
			try:
				skiplist.append({
					'name': entry[0],
					'skips': int(entry[1]),
					'amount': int(entry[2]),
					'guild': ctx.guild.id
				})
			except:
				err += 1
				await ctx.send(f'Couldn\'t parse line "{line}"')
				if err > 10:
					await ctx.send('Too many errors, import cancelled')
					break

		if err <= 10:
			with pymongo.MongoClient(os.environ.get('MONGO')) as client:
				db = client['skips']
				skips = db['slist']
				query = {
					'guild': ctx.guild.id
				}
				skips.delete_many(query)
				skips.insert_many(skiplist)
		
			await message.edit(content='Finished Importing.')





def setup(bot):
	bot.add_cog(simport(bot))