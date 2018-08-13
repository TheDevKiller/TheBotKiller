###########
# Imports #
###########

import discord
from discord.ext import commands
import nekos
import requests
import json
import random

class NSFW:

        def __init__(self, bot):
                self.bot = bot

        @commands.command(aliases=["hentai"], brief="Du bon hentai", usage="(neko|hentai)")
        async def neko(self, ctx, arg):
                if ctx.message.channel.is_nsfw():
                        try:
                                await ctx.send(nekos.img(arg))
                        except nekos.errors.InvalidArgument:
                                await ctx.send("Entre un argument valide :wink:\n Arguments: ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les', 'lewdk', 'ngif', 'meow', 'tickle', 'lewd', 'feed', 'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg', 'pwankg', 'classic', 'kuni', 'pat', '8ball', 'kiss', 'femdom', 'neko', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif', 'smallboobs', 'hug', 'ero']")

                else:
                        await ctx.send("Tu vas choquer des gens :scream: Va dans un salon NSFW !")

        @commands.command(aliases=["ass"], brief="Du bon cul", usage="(cul|ass)")
        async def cul(self, ctx):
                if ctx.message.channel.is_nsfw():
                        lien = "http://media.obutts.ru/{}".format(requests.Session().get("http://api.obutts.ru/butts/0/1/random/").json()[0]["preview"])
                        await ctx.send(lien)
                else:
                        await ctx.send("Tu vas choquer des gens :scream: Va dans un salon NSFW !")
        
        @commands.command(aliases=["boobs"], brief="Des boobs", usage="(seins|boobs)")
        async def seins(self, ctx):
                lien = "http://media.oboobs.ru/{}".format(requests.Session().get("http://api.oboobs.ru/boobs/0/1/random").json()[0]["preview"])
                if ctx.message.channel.is_nsfw():
                    await ctx.send(lien)
                else:
                    await ctx.message.author.send(lien)
                    await ctx.send("Je t'ai envoyé ça en MP {mention}, si tu veux ça dans le salon, va dans un salon NSFW ^^".format(mention=ctx.message.author.mention))


        @commands.command(brief="Du hentai :smiley:", usage="yandere (search|random) [recherche] entre guillemets si il y a des espaces")
        async def yandere(self, ctx, arg1, arg2):
            try:
                if arg1 == "search":
                    recherche = arg2.replace(" ", "+")
                    resultat = requests.get("https://yande.re/post.json?limit=42&tags={}".format(recherche), headers={"User-Agent": "Je suis un gentil bot Discord qui vient en paix :)"}).json()
                    if ctx.message.channel.is_nsfw():
                        await ctx.send(resultat[random.randint(0, 42)]["jpeg_url"])
                    else:
                        await ctx.message.author.send(resultat[random.randint(0, 42)]["jpeg_url"])
                        await ctx.send("Je t'ai envoyé ça en MP {mention}, si tu veux ça dans le salon, va dans un salon NSFW ^^".format(mention=ctx.message.author.mention))
            except:
                        await ctx.send("Aucun résultat pour \"{}\"".format(arg2)) 
def setup(bot):
        bot.add_cog(NSFW(bot))
