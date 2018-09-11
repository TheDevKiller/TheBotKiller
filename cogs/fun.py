###########
# Imports #
###########

import discord
from discord.ext import commands
import requests
import re
import nekos
import random
from bs4 import BeautifulSoup
import random
from PIL import Image, ImageDraw, ImageFont
import json
from pprint import pformat
import pickle
import numpy as np
import subprocess
from pyppeteer import launch

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
        return trad["fr"][txt]


########
# Code #
########

global pom

pom = False

class Fun:
        
    def __init__(self, bot):
            self.bot = bot
            self.jeuJoueurShifumi = None
            self.essais = 0
            self.shifumi = False
            self.joueurShifumi = 1

    # img2txt
    @commands.command(usage="img2txt with attachment")
    async def img2txt(self, ctx):

        try:
            url = ctx.message.attachments[0].url
        except:
            await ctx.send("I need an image !")

        image = requests.Session().get(url).content

        fichier = ctx.message.attachments[0].filename

        with open(fichier, "wb") as file:
                file.write(image)

        im = Image.open(fichier)

        im = im.convert(mode="L")

        im.save()

        im.close(filename)

    # Cookie
    @commands.command(usage="cookie mention")
    async def cookie(self, ctx, arg):
        await ctx.send(getmsg(ctx, "cookiemsg"))

    # VDM
    @commands.command(aliases=["viedemerde"], usage="(viedemerde|vdm)")
    async def vdm(self, ctx):
            source = requests.Session().get("https://www.viedemerde.fr/aleatoire", headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}).content
            soup = BeautifulSoup(source, "html.parser")
            vdm = list(random.choice(soup.find_all("p", class_="block hidden-xs")).children)[1].string 
            await ctx.send(vdm.replace(" VDM", ""))

    # DTC
    @commands.command(aliases=["danstonchat"], usage="(dtc|danstonchat)")
    async def dtc(self, ctx):
        source = requests.get("https://www.danstonchat.com/random0.html").content
        soup = BeautifulSoup(source, "html.parser")
        lst = soup.find_all("div", class_="addthis_inline_share_toolbox")
        await ctx.send(random.choice(lst)["data-description"])

    # Ah
    @commands.command(usage="ah")
    async def ah(self, ctx):
            with open("img/ah.jpg", "rb") as img:
                    await ctx.send(file=discord.File(img))

    # Obvious
    @commands.command(usage="obvious")
    async def obvious(self, ctx):
            with open("img/obvious.jpg", "rb") as img:
                    await ctx.send(file=discord.File(img))
    # Non
    @commands.command(aliases=["non"], usage="non")
    async def no(self, ctx):
            with open("img/non.jpg", "rb") as img:
                    await ctx.send(file=discord.File(img))

    # Chat
    @commands.command(aliases=["chat"], usage="(chat|cat)")
    async def cat(self, ctx):
            chaturl = nekos.cat()
            await ctx.send(chaturl)

    # Shifumi
    @commands.command(name="shifumi", usage="shifumi")
    async def _shifumi(self, ctx):

        # Partie de Shifumi en cours
        self.shifumi = True

        # Joueur
        self.joueurShifumi = ctx.message.author

        # Message joue, à modifier
        self.messageJoue = await ctx.send(embed=discord.Embed(title="Shifumi", description="Joue :wink:", color=0xff7400))

        # Réactions
        await self.messageJoue.add_reaction("🌑")
        await self.messageJoue.add_reaction("📄")
        await self.messageJoue.add_reaction("✂")

    # Dis
    @commands.command(aliases=["dis"], usage="(dis|say) message")
    async def say(self, ctx, *, arg):
            await ctx.send(arg)

    # Website screen
    @commands.command(usage="websitescreen url", aliases=["sitescreen", "wsb", "wb"])
    async def websitescreen(self, ctx, *, url):

        browser = await laucnh()
        page = await browser.newPage()

        if "file:///" not in url:
            await page.goto(url)
        else:
            await ctx.send("Méchant !")

        await page.screenshot({"tmp": "screen.png!"})

    # Martine
    @commands.command(usage="martine imageName text")
    async def martine(self, ctx, image, *, texte):

        image = image.lower()

        imageList = ['ecole', 'surprise', 'lanterne', 'train', 'camping', 'menage', 'ferme', 'zoo', 'fantome', 'contes', 'ours', 'rentree', 'princesse', 'maman', 'voyage', 'accident', 'noel', 'demenage', 'avion', 'theatre', 'mongolfiere']

        if image not in imageList:

            n = "\n"
            await ctx.send(f"Liste des images disponibles:{n}{n}- {f'{n}- '.join(imageList)}")

        else:
            for i, e in enumerate(imageList):
                if e == image:
                    imageNbre = i

            source = requests.get(f"http://www.retourdemartine.free.fr/create2.php?t={texte}&m={imageNbre+1}", headers={"User-Agent": "Un gentil bot discord"}).content

            soup = BeautifulSoup(source, "html.parser")

            imgUrl = "http://www.retourdemartine.free.fr/" + soup.find("img", class_="blackborder")["src"]

            await ctx.send(imgUrl)

    # Pi
    @commands.command(usage="pi number")
    async def pi(self, ctx, nbre):

        pi = "141592653589"

        if nbre in pi:
            for i, e in enumerate(pi):
                if e == nbre[0]:
                    if pi[i:i+len(nbre)] == nbre:
                        await ctx.send(f"Le nombre se trouve à la {i+1}ème décimale de pi")
                        if i-5 < 0:
                            await ctx.send(pi[0:i+len(nbre)+5])
                        elif i+len(nbre)+5 > len(pi):
                            await ctx.send(pi[i-5:])
                        else:
                            await ctx.send(pi[i-5:i+len(nbre)+5])
                        break

        else:
            await ctx.send(f"Votre nombre n'est pas dans les {len(pi)} premières décimales de pi")

    # Réactions
    async def on_reaction_add(self, reaction, user):
        
        reactionValides = ["🌑", "📄", "✂"]

        if self.shifumi == True:
            if self.joueurShifumi == user:
                if reaction.emoji in reactionValides:

                    jeuJoueur = reaction.emoji

                    # Jeu du bot
                    elements = ["🌑", "📄", "✂"]
                    elementBot = random.choice(elements)

                    # Possibilités pour voir les gagnants
                    jeux = \
                    {"🌑": ["✂"],
                    "✂": ["📄"],
                    "📄": ["🌑"]}

                    # Check de qui a gagné
                    if jeuJoueur == elementBot:
                            resultat = "Égalité :neutral_face:"
                    elif elementBot in jeux[jeuJoueur]:
                            resultat = "T'as gagné :frowning:"
                    else:
                            resultat = "T'as perdu :smiley:"

                    # Édition du message
                    em = discord.Embed(title=f"Résultat du sifumi entre {self.joueurShifumi.name} et </TheBotKiller>", color=0xff7400)
                    em.add_field(name="Tu as joué", value=f"{getmsg(reaction, jeuJoueur)} {jeuJoueur}")
                    em.add_field(name="J'ai joué", value=f"{getmsg(reaction, elementBot)} {elementBot}")
                    em.add_field(name="Résultat", value=resultat)
                    await self.messageJoue.edit(embed=em)

def setup(bot):
        bot.add_cog(Fun(bot)) 