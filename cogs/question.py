# ????

from discord.ext import commands
import discord
import os

class cipher(commands.Cog):

  def __init__(self, bot):
    self.bot = bot


  @commands.command(name='how')
  async def _part1(self, ctx):
    await ctx.send('RISNC DOSZU TNAMT ADZTH TSAHC MZYNS COWSI ZTTIA ANNES PGEEM IPNZ')
  
  @commands.command(name=os.getenv('A1'))
  @commands.dm_only()
  async def _part2(self, ctx):
    await ctx.send(os.getenv('Q2'))
  # not real chinese?
  
  @commands.command(name=os.getenv('A2'))
  @commands.dm_only()
  async def _part3(self, ctx):
    await ctx.send(os.getenv('Q3'))
  # .png? .txt?

  @_part2.error
  @_part3.error
  async def notInDM(self, ctx, error):
    pass



def setup(bot):
  bot.add_cog(cipher(bot))