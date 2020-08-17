 # terrible code™ by nochef
# my user id: 290983149507182592 (apple#9999)

# now with multiple server support!!!!!!!
# yay!!!!!

# to do:
# idk
# put json docs into a folder and modify pys to work
# make a import command that uses ONLY exported file format and uses insert_many for much improved speed

import os
import json
from discord.ext import commands


# prefix handling

def get_prefix(bot, message): # load prefix
	with open('storage/prefixes.json', 'r') as f:
		prefixes = json.load(f)
	if not message.guild:
		return '?'
	guildPrefix = prefixes.get(str(message.guild.id))
	return guildPrefix

def get_channel(ctx):
	with open('storage/channels.json', 'r') as f:
		channels = json.load(f)
	return channels.get(str(ctx.guild.id))


bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True)
bot.remove_command('help')

# add prefix on guild join
@bot.event
async def on_guild_join(guild):
	print('joined ' + str(guild.id))
	with open('storage/prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = '?'

	with open('storage/prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent = 2)
	
	for channel in guild.text_channels:
		if channel.permissions_for(guild.me).send_messages:
			await channel.send('Hello! Type `?help skip` to setup skipping or `?skipprefix <new prefix>` to change to prefix.')
		break


# remove prefix and channel on guild leave
@bot.event
async def on_guild_remove(guild):
	print('left ' + str(guild.id))
	with open('storage/prefixes.json', 'r') as f:
		prefixes = json.load(f)

	with open('storage/channels.json', 'r') as g:
		channels = json.load(g)

	with open('storage/amounts.json', 'r') as h:
		amounts = json.load(h)

	prefixes.pop(str(guild.id))
	channels.pop(str(guild.id))
	amounts.pop(str(guild.id))

	with open('storage/prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent = 2)

	with open('storage/channels.json', 'w') as g:
		json.dump(channels, g, indent = 2)

	with open('storage/amounts.json', 'w') as h:
		json.dump(amounts, h, indent = 2)


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
			await ctx.send(f'{type(e).__name__}: {e})

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
			await ctx.send(f'{type(e).__name__}: {e})
			
# ready

@bot.event
async def on_ready():
	print('\n' + bot.user.name + ' online\n' + str(bot.user.id) + '\n---------------')


# run bot

bot.run(os.environ.get('TOKEN')) 
# the token ends with 'c' if you were wondering
