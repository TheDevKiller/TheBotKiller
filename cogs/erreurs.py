###########
# Imports #
###########

import discord
from discord.ext import commands

########
# Code #
########

class Erreurs:

        def __init__(self, bot):
                self.bot = bot
        
                # Erreur
        async def on_error(event, *args, **kwargs):
                message = args[0]
                await message.channel.send(embed=discord.Embed(title="C'est con !", description="```python\n{}\n```".format(traceback.format_exc()), color=0xff0000).set_footer(text="Ce message s'auto-détruira dans 1 min"), delete_after=60.0)

                em = discord.Embed(title="C'est con !", description="```python\n{}\n```".format(traceback.format_exc()), color=0xff0000)

                await thedevkiller.send(embed=em)

                # Erreurs de commande
        async def on_command_error(self, ctx, ex):
                if isinstance(ex, commands.MissingRequiredArgument) or isinstance(ex, commands.BadArgument):
                        await ctx.send("Utilisation de la commande:\n```\n{}\n```".format(ctx.command.usage))           
                elif isinstance(ex, commands.CommandNotFound):
                        pass
                else:
                        await ctx.send(ex)              
        
        @commands.command(aliases=["error"], brief="Provoque une erreur", usage="(erreur|error)", hidden=True)
        async def erreur(self, ctx):
                raise NameError("Erreur !")

def setup(bot):
        bot.add_cog(Erreurs(bot))

