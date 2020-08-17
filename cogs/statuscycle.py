# for changing the bot's status periodically

import discord
from discord.ext import commands, tasks
from random import choice


class status(commands.Cog):
	
	def __init__(self, bot):
		if self.statusCycle.is_running():
			self.statusCycle.restart()
		else:
			self.statusCycle.start()
		self.bot = bot
		self.status = ['https://github.com/noshef/skipBot','bruh',  'i have no life', 'can i skip?', '?skip notch', 'who is nochef', 'else: if:', 'you win a cookie', '@everyone', 'time for a skip giveaway', 'i love ronsted', 'oops bot is down', 'yeah', 'this level got buffed', 'friend me on hypixel', 'badlion client', 'goodlion client', 'does anyone read these', 'i have gained sentience', 'hi soupity', 'nice skin bro']  

	@tasks.loop(seconds=10)
	async def statusCycle(self):
		await self.bot.change_presence(
			status = discord.Status.idle,
			activity = discord.Game(name=choice(self.status)))


def setup(bot):
	bot.add_cog(status(bot))
