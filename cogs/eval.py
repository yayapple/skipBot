# only me command haha

from discord.ext import commands
import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout

class _eval(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='eval')
	async def _eval(self, ctx, *, body):
		
		if not ctx.author.id == 290983149507182592:
			await ctx.send('You must be me to use that command!')

		env = {
			'ctx': ctx,
			'bot': self.bot,
			'channel': ctx.channel,
			'author': ctx.author,
			'guild': ctx.guild,
			'message': ctx.message,
			'source': inspect.getsource
		}

		banned = [
			'environ.',
			'getenv(',
			'.env',
			'while True',
			'eval(',
			'exec('
		]

		if any(substring in body for substring in banned):
			await ctx.send('no')
			return

		def cleanup_code(content):
			"""Automatically removes code blocks from the code."""
			# remove ```py\n```
			if content.startswith('```') and content.endswith('```'):
				return '\n'.join(content.split('\n')[1:-1])

			# remove `foo`
			return content.strip('` \n')

		env.update(globals())

		body = cleanup_code(body)
		stdout = io.StringIO()
		err = out = None

		to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

		try:
			exec(to_compile, env)
		except Exception as e:
			err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
			return await ctx.message.add_reaction('\u2049')

		func = env['func']
		try:
			with redirect_stdout(stdout):
				ret = await func()
		except:
			value = stdout.getvalue()
			err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
		else:
			value = stdout.getvalue()
			if ret is None:
				if value:
					if len(value) > 500:
						value = value[:499] + '\n\n    Output Clipped '
					out = await ctx.send(f'```py\n{value}\n```')

			else:
				bruh = value + ret
				if len(bruh) > 500:
					bruh = bruh[:499] + '\n\n    Output Clipped'
				out = await ctx.send(f'```py\n{bruh}\n```')

		if out:
			await ctx.message.add_reaction('\u2705')  # tick
		elif err:
			await ctx.message.add_reaction('\u2049')  # x
		else:
			await ctx.message.add_reaction('\u2705')

def setup(bot):
	bot.add_cog(_eval(bot))