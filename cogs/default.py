# a command to set the default amount of skips in a server.

import json
from discord.ext import commands
import discord

def get_default(ctx):
	with open('storage/amounts.json', 'r') as f:
		amounts = json.load(f)
	return amounts.get(str(ctx.guild.id))

class default(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	

	@commands.command(aliases=['default'])
	async def setdefault(self, ctx, *args):

		if not ctx.author == ctx.guild.owner and not discord.utils.get(ctx.guild.roles, name="Trusted") in ctx.author.roles:
			return await ctx.send('You must be the server owner to do that!')

		if len(args) != 1 or not args[0].isdigit():
			return await ctx.send('Please enter a valid number!')
	
		with open('storage/amounts.json', 'r') as f:
			amounts = json.load(f)

		amounts[str(ctx.guild.id)] = int(args[0])

		with open('storage/amounts.json', 'w') as f:
			json.dump(amounts, f, indent = 2)

		await ctx.send(f'Set default skip amount to {args[0]}. Any skip entries before now will still have the prevous skip amount.')




def setup(bot):
	bot.add_cog(default(bot))