# various help commands

import discord
from discord.ext import commands
from main import get_config

class bothelp(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def help(self, ctx, *command):
		if command in (('skip',), ('skips',)):
			prefix = get_config(ctx).get('prefix')

			embed = discord.Embed(
				title="Skipping", 
				color=discord.Color.gold())

			embed.add_field(
				name='Setup',
				value="""
				`{0}whitelist`: Choose a channel in which skips can be performed. Make sure guests and res cannot send messages in the channel. (Admin)
				`{0}default` [num]: Sets the amount of skips people start out with. [try to only set this once] (Server Owner)
				""".format(prefix),
				inline=True
				)
			embed.add_field(
				name='Skipping',
				value="""
				`{0}skip` or `{0}s` [name]: Brings up the skip menu. In the menu, react with ⏩ to skip the player, or react ➕ to allow one more skip for the player.
				`{0}delskip` or `{0}d` [name]: Brings up a menu similar to the skip menu, except for deleting skips instead of adding them.
				""".format(prefix),
				inline=False
				)
			embed.add_field(
				name='Other',
				value="""
				`{0}reset`: Deletes ALL skips from the database. Cannot undo. (Server Owner)
				`{0}export`: Export all the skips into a text file. (Admin)
				`{0}import`: Export skips from a text file. Deletes current skips in the process. (Server Owner)

				For other users to use owner only commands, create a role called "Trusted" and assign it to them. Make sure it is near the top so that others may not assign it to themselves.
				""".format(prefix),
				inline=False
				)
			
			embed.set_footer(text="https://repl.it/@nochef/skipBot")

			await ctx.send(embed=embed)
			return

		
		prefix = get_config(ctx).get('prefix')

		embed = discord.Embed(
			title="skipBot Help", 
			color=discord.Color.gold()
		)

		embed.add_field(
			name='Skip Commands',
			value="""
			`{0}skip` or `{0}s` [name]: Brings up the skip menu (say `{0}help skip` for more info)
			`{0}delskip` or `{0}d` [name]: Brings up the skip deletion menu.
			`{0}export`: Exports skips into a file.
			`{0}import`: Imports skips from a file. (Deletes current skips in the database)
			`{0}whitelist`: Changes the channel in which the skip command works 
			`{0}default`: Sets the default amount of skips players will recieve. 
			""".format(prefix),
			inline=True
			)

		embed.add_field(
			name='Other Commands',
			value="""
			`{0}prefix` or `{0}skipPrefix` [new prefix]: Changes the prefix
			`{0}help`: Brings up this menu
			`{0}ping`: Shows bot ping
			`{0}joke`: Says a Club Penguin joke
			`{0}invite`: Sends the bot invite
			""".format(prefix),
			inline=False
			)
		
		embed.set_footer(text="https://repl.it/@nochef/skipBot")

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(bothelp(bot))
