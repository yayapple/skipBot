# misc commands unrelated to skipping.

import discord
from discord.ext import commands
import json
from main import get_prefix

class misc(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	# prefix command

	@commands.command(aliases=['skipPrefix'])
	@commands.has_permissions(administrator=True)
	async def prefix(self, ctx, *prefix):

		if len(prefix) != 1:
			return await ctx.send('Please enter a valid prefix.')

		with open('storage/prefixes.json', 'r') as f:
			prefixes = json.load(f)

		prefixes[str(ctx.guild.id)] = prefix[0]

		with open('storage/prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent = 2)
		
		await ctx.send(f'changed prefix to "{prefix}"')

	@prefix.error
	async def permsError(ctx, error):	
		if isinstance(error, commands.MissingPermissions):
			await ctx.send('You must be an administrator to use that command.')

	# invite command

	@commands.command()
	async def invite(self, ctx):
		embed = discord.Embed(
			title = "Invite link", 
			color = discord.Color.gold(),
			description = '[Click here to invite the bot](https://discord.com/oauth2/authorize?client_id=711998861165592728&permissions=8&scope=bot)')
		await ctx.send(embed=embed)
	

	# ping command

	@commands.command()
	async def ping(self, ctx):
		ping = int(self.bot.latency * 1000)
		embed = discord.Embed(
			title = "Pong", 
			color = discord.Color.gold(),
			description = f"{ping}ms")
		await ctx.send(embed=embed)
	
def setup(bot):
	bot.add_cog(misc(bot))