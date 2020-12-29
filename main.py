# terrible code™ by nochef
# my user id: 290983149507182592 (apple#9999)

# now with multiple server support!!!!!!!
# yay!!!!!

# to do:
# instead of calling updateDict and then updating the database, add updating the database to updateDict()

import os
import json
from discord.ext import commands
import pymongo


# prefix handling

def get_prefix(bot, message): # load prefix
	with pymongo.MongoClient(os.environ.get('MONGO')) as client:
		db = client['skips']
		config = db['guild config']

		guildEntry = config.find_one({'guild': message.guild.id})
		if guildEntry is None:
			guildPrefix = '?'
		else:
			guildPrefix = guildEntry.get('prefix')

	return guildPrefix

entryDict = {}

def get_data():
	with pymongo.MongoClient(os.getenv('MONGO')) as client:
		db = client['skips']
		config = db['guild config']
				
		for entry in list(config.find()):
			entryDict.update({
				entry.get('guild'): {
					'prefix': entry.get('prefix'),
					'channel': entry.get('channel'),
					'default': entry.get('default')
				}
			})
			
	print(entryDict)

def updateDict(ctx, key, value):
	entryDict.get(ctx.guild.id).update({key: value})

def addEntry(guild):
	entryDict.update({
		guild.id: {
			'prefix': '?',
			'channel': '',
			'default': ''
		}
	})

def get_config(ctx):
	if not entryDict:
		get_data()
	return entryDict.get(ctx.guild.id)



bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True)
bot.remove_command('help')

# add prefix on guild join
@bot.event
async def on_guild_join(guild):

	addEntry(guild)

	with pymongo.MongoClient(os.environ.get('MONGO')) as client:
		db = client['skips']
		config = db['guild config']
		
		config.insert_one({
			'guild': guild.id,
			'prefix': '?',
			'default': '',
			'channel': ''
		})
	
	for channel in guild.text_channels:
		if channel.permissions_for(guild.me).send_messages:
			await channel.send('Hello! Type `?help skip` to setup skipping or `?skipprefix <new prefix>` to change to prefix.')
		break


# remove prefix and channel on guild leave
@bot.event
async def on_guild_remove(guild):
	print('left ' + str(guild.id))
	with pymongo.MongoClient(os.environ.get('MONGO')) as client:
		db = client['skips']
		config = db['guild config']

		config.delete_one({'guild': guild.id})

### COG COMMANDS ###

for filename in os.listdir('./cogs'):
	if filename.endswith('.py') and filename not in ['import.py']:
		bot.load_extension(f'cogs.{filename[:-3]}')

# load, unload, reload cogs

@bot.command(aliases=['l'])
async def load(ctx, extension):
	if not ctx.author.id == 290983149507182592:
		return
	else:
		try:
			bot.load_extension(f'cogs.{extension}')
			await ctx.send(f'loaded {extension}')
		except Exception as e:
			await ctx.send(f'{type(e).__name__}: {e}')

@bot.command(aliases=['ul', 'u'])
async def unload(ctx, extension):
	if not ctx.author.id == 290983149507182592:
		return
	else:
		bot.unload_extension(f'cogs.{extension}')
		await ctx.send(f'unloaded {extension}')

@bot.command(aliases=['rl', 'r'])
async def reload(ctx, extension):
	if not ctx.author.id == 290983149507182592:
		return
	else:
		try:
			bot.unload_extension(f'cogs.{extension}')
			bot.load_extension(f'cogs.{extension}')
			await ctx.send(f'reloaded {extension}')
		except Exception as e:
			await ctx.send(f'{type(e).__name__}: {e}')

# ready

@bot.event
async def on_ready():
	print('\n' + bot.user.name + ' online\n' + str(bot.user.id) + '\n---------------')


# run bot

bot.run(os.environ.get('TOKEN')) 
# the token ends with 'c' if you were wondering
