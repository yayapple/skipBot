from discord.ext import commands
import os

bot = commands.Bot(command_prefix = '[')

@bot.command()
async def ping(ctx):
	await ctx.send('pong')

@bot.command(aliases=['l'])
async def load(ctx, extension):
	if not ctx.author.id == 290983149507182592:
		return
	bot.load_extension(f'cogs.{extension}')
	await ctx.send(f'loaded {extension}')

@bot.command(aliases=['ul', 'u'])
async def unload(ctx, extension):
	if not ctx.author.id == 290983149507182592:
		return
	bot.unload_extension(f'cogs.{extension}')
	await ctx.send(f'unloaded {extension}')


for filename in os.listdir('./cogs'):
	if filename.endswith('.py') and filename not in ['import.py']:
		bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
	print('\n' + bot.user.name + ' online')
	print(bot.user.id)
	print('---------------')

bot.run(os.getenv('TOKEN'))