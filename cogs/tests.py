###########
# Imports #
###########

import discord
from discord.ext import commands
import json

#############
# Variables #
#############

with open("trads.json", "r") as fichier:
    trad = json.loads(fichier.read())

########
# Code #
########

class Tests:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hw(self, ctx):
        with open("config.json", "r") as fichier:
            config = json.loads(fichier.read())
        await ctx.send(trad[config[str(ctx.message.guild.id)]["lang"]]["hw"])

def setup(bot):
    bot.add_cog(Tests(bot))
