##########
# Import #
##########

import discord
from discord.ext import commands
from zalgo_text import zalgo

########
# Code #
########

class Texte:
        
    def __init__(self, bot):
        self.bot = bot

    # Lower
    @commands.command(usage="lower \"texte\", entre guillemets si il y a des espaces")
    async def lower(self, ctx, *, arg):
        await ctx.send(arg.lower())
        
    # Upper
    @commands.command(usage="upper \"texte\", entre guillemets si il y a des espaces")
    async def upper(self, ctx, *, arg):
        await ctx.send(arg.upper())

    # Capitalize
    @commands.command(usage="capitalize \"texte\", entre guillemets si il y a des espaces")
    async def capitalize(self, ctx, *, arg):
        await ctx.send(arg.capitalize())

    # Title
    @commands.command(usage="title \"texte\", entre guillemets si il y a des espaces")
    async def title(self, ctx, *, arg):
        await ctx.send(arg.title())

    # Glitch
    @commands.command(aliases=["zalgo"], usage="(glitch|zalgo) text")
    async def glitch(self, ctx, *, arg):
        await ctx.send(zalgo.zalgo().zalgofy(arg))

def setup(bot):
    bot.add_cog(Texte(bot))