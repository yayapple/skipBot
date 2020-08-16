from discord.ext import commands
import os

bot = commands.Bot(command_prefix = '[')

@bot.command
async def ping(ctx):
    await ctx.send('pong')


@bot.event
async def on_ready():
    print('\n' + bot.user.name + ' online')
	print(bot.user.id)
	print('---------------')

bot.run(os.getenv('TOKEN'))