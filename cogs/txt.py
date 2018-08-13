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

    @commands.command(brief="Votre texte en minuscule :smiley:", usage="lower \"texte\", entre guillemets si il y a des espaces")
    async def lower(self, ctx, arg):
        await ctx.send(arg.lower())
        
    @commands.command(brief="Votre texte en majuscules :smiley:", usage="upper \"texte\", entre guillemets si il y a des espaces")
    async def upper(self, ctx, arg):
        await ctx.send(arg.upper())

    @commands.command(brief="Votre texte avec un majuscule au début :smiley:", usage="capitalize \"texte\", entre guillemets si il y a des espaces")
    async def capitalize(self, ctx, arg):
        await ctx.send(arg.capitalize())

    @commands.command(brief="Votre texte avec une lettre à chaque mot :smiley:", usage="title \"texte\", entre guillemets si il y a des espaces")
    async def title(self, ctx, arg):
        await ctx.send(arg.title())

    @commands.command(aliases=["zalgo"], brief="Votre texte glitché avec Zalgo", usage="zalgo \"texte\", le texte doit être entre guillemets si il y a des espaces")
    async def glitch(self, ctx, arg):
        await ctx.send(zalgo.zalgo().zalgofy(arg))

def setup(bot):
    bot.add_cog(Texte(bot))
                
