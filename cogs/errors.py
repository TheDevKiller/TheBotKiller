###########
# Imports #
###########

import discord
from discord.ext import commands
import json

#############
# Fonctions #
#############

# Obtenir une traduction
def getmsg(ctx, txt):

    # Config
    with open("config.json", "r") as fichier:
        config = json.loads(fichier.read())

    # Ouvrir le fichier de traductions
    with open("trads.json", "r") as fichier:
        trad = json.loads(fichier.read())

    try:
        return trad[config[str(ctx.message.guild.id)]["lang"]][txt]

    except:
        return trad["en"][txt]

########
# Code #
########

class Errors:

        def __init__(self, bot):
            self.bot = bot

        # Erreurs de commande
        async def on_command_error(self, ctx, ex):

                if isinstance(ex, commands.CommandNotFound):
                    pass

                #if isinstance(ex, commands.MissingRequiredArgument) or isinstance(ex, commands.BadArgument):
                
                else:
                    em = discord.Embed(title=getmsg(ctx, "commanderrortitle"), description=f"`{ctx.command.usage}`", color=0xEA2027)
                    em.set_footer(text=getmsg(ctx, "commanderrorfooter"))
                    await ctx.send(embed=em)
                    print(ex)

                # else:
                #     await ctx.send(ex)
        

        # Erreur
        @commands.command(aliases=["erreur"], usage="(erreur|error)", hidden=True)
        async def error(self, ctx):
                raise NameError("Error !")

def setup(bot):
        bot.add_cog(Errors(bot))
