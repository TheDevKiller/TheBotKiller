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
from pyppeteer.errors import *

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

    # ACCapture
    @commands.command(usage="accapture")
    async def accapture(self, ctx):
        with open("accapture.json") as file:
            messages = json.loads(file.read())
        choice = random.choice(list(messages.keys()))
        em = discord.Embed(title=f"Tu as attrapé un {choice}", description=messages[choice], color=0x00FF00)
        await ctx.send(embed=em)

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

    # Website screen
    # @commands.command(usage="websitescreen url", aliases=["sitescreen", "ws"])
    # async def websitescreen(self, ctx, *, url):
    #     if not url.startswith("http"):
    #         await ctx.send("Méchant !")
    #         return
    #     try:
    #         browser = await launch()
    #         page = await browser.newPage()
    #         await page.setViewport({"width": 1366, "height": 768})
    #         await page.goto(url)
    #         await page.screenshot({"path": "screen.png"})
    #     except TimeoutError:
    #         await ctx.send("Alala la co' en carton (Timeout)")
    #         return
    #     # except ClientOSError:
    #     #     await ctx.send("Petit bug :sweat_smile: (Connection reset by peer)")
    #     #     return
    #     except PageError as ex:
    #         ex = str(ex)
    #         if ex.startswith("net::ERR_CERT_COMMON_NAME_INVALID"):
    #             await ctx.send("Certificat SSL incorrect ou expiré")
    #         elif ex.startswith("net::ERR_CONNECTION_REFUSED"):
    #             await ctx.send("Connexion refusée")
    #         return
    #     except Exception as ex:
    #         await ctx.send(f"Un erreur inconnue est survenue ! ({ex})")
    #         return
    #     finally:
    #         await browser.close()
    #     await ctx.send(file=discord.File("screen.png"))

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

def setup(bot):
        bot.add_cog(Fun(bot)) 