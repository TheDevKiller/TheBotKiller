###########
# Imports #
###########

import discord
from discord.ext import commands
import requests
import re
import nekos
import random

########
# Code #
########

global pom

pom = False

class Fun:
        
        def __init__(self, bot):
                self.bot = bot
        
        @commands.command(aliases=["viedemerde"], brief="Vie de merde", usage="(viedemerde|vdm)")
        async def vdm(self, ctx):
                source = requests.Session().get("https://www.viedemerde.fr/aleatoire", headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}).content
                vdm = re.search(r"<p class=\"block hidden-xs\">\n<a href=\".*\">\n(.*) VDM", source.decode())[1]
                await ctx.send(vdm)

        @commands.command(brief="Ah !", usage="ah")
        async def ah(self, ctx):
                with open("img/ah.jpg", "rb") as img:
                        await ctx.send(file=discord.File(img))

        @commands.command(brief="Merci Captain Obvious !", usage="obvious")
        async def obvious(self, ctx):
                with open("img/obvious.jpg", "rb") as img:
                        await ctx.send(file=discord.File(img))

        @commands.command(brief="Non !", usage="non")
        async def non(self, ctx):
                with open("img/non.jpg", "rb") as img:
                        await ctx.send(file=discord.File(img))

        @commands.command(aliases=["cat"], brief="Trop mignon <3", usage="(chat|cat)")
        async def chat(self, ctx):
                chaturl = nekos.cat()
                await ctx.send(chaturl)

        @commands.command(brief="Pierre, feuille, ciseaux", usage="shifumi")
        async def shifumi(self, ctx):
                messageJoue = await ctx.send(embed=discord.Embed(title="Shifumi", description="Joue :wink:", color=0xff7400))

                await messageJoue.add_reaction("🌑")
                await messageJoue.add_reaction("📄")
                await messageJoue.add_reaction("✂")

                reactionsValides = ["🌑", "📄", "✂"]

                reaction = await self.bot.wait_for("reaction_add", check=lambda r, u: u.id == ctx.message.author.id)

                print(reaction[1].id)

                while reaction[0].emoji not in reactionsValides:
                        await ctx.send("Réagis avec pierre, feuille ou ciseaux :wink:")
                        reaction = await bot.wait_for("reaction_add", check=lambda r, u: u.id == ctx.message.author.id)

                while reaction[1].id != ctx.message.author.id:
                        await ctx.send("C'est là je vais mettre le nom du joueur logiquement qui a lancé la partie, pas toi ! :stuck_out_tongue_winking_eye:")
                        reaction = await bot.wait_for("reaction_add", check=lambda r, u: u.id == ctx.message.author.id)

                if reaction[0].emoji == "🌑":
                        jeuJoueur = "pierre :new_moon:"
                elif reaction[0].emoji == "📄":
                        jeuJoueur = "feuille :page_facing_up:"
                elif reaction[0].emoji == "✂":
                        jeuJoueur = "ciseaux :scissors:"

                elements = ["pierre :new_moon:", "feuille :page_facing_up:", "ciseaux :scissors:"]
                elementBot = random.choice(elements)

                jeux = \
                {"pierre :new_moon:": ["ciseaux :scissors:"],
                "ciseaux :scissors:": ["feuille :page_facing_up:"],
                "feuille :page_facing_up:": ["pierre :new_moon:"]}

                if jeuJoueur == elementBot:
                        resultat = "Égalité :neutral_face:"
                elif elementBot in jeux[jeuJoueur]:
                        resultat = "T'as gagné :frowning:"
                else:
                        resultat = "T'as perdu :smiley:"

                await messageJoue.edit(embed=discord.Embed(title="Résultat du Shifumi entre " + ctx.message.author.name + " et </TheBotKiller>", description="** **\n**Tu as joué: **\n\n" + jeuJoueur.capitalize() + "\n\n**J'ai joué: **\n\n" + elementBot.capitalize() + "\n\n**Résultat: **\n\n" + resultat, color=0xff7400))

                if resultat == "Égalité :neutral_face:":
                        gagnant = "Aucun"
                elif resultat == "T'as gagné :frowning:":
                        gagnant = ctx.message.author.name
                else:
                        gagnant = "</TheBotKiller>"

                jeuJoueur = jeuJoueur.split(" ")[0]
                elementBot = elementBot.split(" ")[0]

        @commands.command(aliases=["say"], brief="Dis quelque chose", usage="\"message\", le message doit être entre guillemets si il y a des espaces")
        async def dis(self, ctx, arg):
                await ctx.send(arg)

        @commands.command(aliases=["plusoumoins", "+-", "+ou+"], brief="Plus ou moins", usage="(+-|+ou-|plusoumoins|pom) <min> <max>")
        async def pom(self, ctx, pmin, pmax):
                global joueurPom
                global minpom
                global maxpom
                global nbre
                global pomchan
                global essais
                global pom
                minpom = pmin
                maxpom = pmax   
                joueurPom = ctx.message.author
                if(minpom > maxpom):
                        minpom, maxpom = maxpom, minpom
                await ctx.send("Devine à quel nombre je pense entre {} et {}".format(minpom, maxpom))
                nbre = random.randint(int(minpom), int(maxpom))
                pomchan = ctx.message.channel
                pom = True
                essais = 1
        
        async def on_message(self, message):
                global essais
                
                if pom == True and message.author == joueurPom and message.channel == pomchan:
                        nbreJoueur = int(message.content)
                        if nbreJoueur < nbre:
                                await message.channel.send("C'est plus !")
                                essais += 1
                        elif nbreJoueur > nbre:
                                await message.channel.send("C'est moins !")
                                essais += 1
                        elif nbreJoueur == nbre:
                                if essais <= 1:
                                        await message.channel.send("C'est ça, bien joué {mention} ! Tu as réussi en {essais} essais".format(mention=message.author.mention, essais=essais))
                                else:
                                        await message.channel.send("C'est ça, bien joué {mention} ! Tu as réussi en {essais} essais".format(mention=message.author.mention, essais=essais))
                                plusoumoins = False
 
def setup(bot):
        bot.add_cog(Fun(bot))
