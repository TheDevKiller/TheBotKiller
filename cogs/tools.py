###########
# Imports #
###########

import discord
from discord.ext import commands
import requests
import qrcode
import os
import pytesseract
from PIL import Image
import json
import random

#############
# Variables #
#############

with open("secrets.json", "rb") as secretsFile:
        secrets = json.load(secretsFile)

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

    return trad[config[str(ctx.message.guild.id)]["lang"]][txt]

########
# Code #
########

class Tools:
        
        def __init__(self, bot):
                self.bot = bot

                self.qr = qrcode.QRCode( # Paramètres du QR Code
                        version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2
                )

        # Todo
        @commands.command(usage="todo (add|remove|modify|view) [number] text")
        async def todo(self, ctx, action="view", *, text=""):
            if action == "add":

                text = text.capitalize()

                with open("todo.json", "r") as file:
                    dico = json.loads(file.read())

                if str(ctx.message.author.id) in dico:


                    if isinstance(dico[str(ctx.message.author.id)], list):
                        dico[str(ctx.message.author.id)].append(text)

                    else:
                        dico[str(ctx.message.author.id)] = []
                        dico[str(ctx.message.author.id)].append(text)

                else:
                    dico[str(ctx.message.author.id)] = []
                    dico[str(ctx.message.author.id)].append(text)

                with open("todo.json", "w") as file:
                    file.write(json.dumps(dico, indent=4))

            elif action == "view":

                with open("todo.json", "r") as file:
                    dico = json.loads(file.read())

                try:
                    description = ""
                    for i, e in enumerate(dico[str(ctx.message.author.id)]):
                        description += "%s. %s\n"%(i+1, e)

                    em = discord.Embed(title=getmsg(ctx, "todotitlembed"), description=description, color=0xff6600)
                    await ctx.send(embed=em)

                except KeyError:
                    await ctx.send(getmsg(ctx, "todotitlembed"))

            elif action == "remove":

                nbre = int(text.split(" ")[0])

                with open("todo.json", "r") as file:
                    dico = json.loads(file.read())

                del dico[str(ctx.message.author.id)][nbre - 1]

                with open("todo.json", "w") as file:
                    file.write(json.dumps(dico, indent=4))

            elif action == "modify":

                with open("todo.json", "r") as file:
                    dico = json.loads(file.read())

                nbre = int(text.split(" ")[0])

                texte = ""

                for e in text.split(" ")[1:]:
                    texte += e + " "

                dico[str(ctx.message.author.id)][nbre - 1] = texte

                with open("todo.json", "w") as file:
                    file.write(json.dumps(dico, indent=4))

                await ctx.send("")

        # Report
        @commands.command(aliases=["bug"], brief="Signaler un bug", usage="(report|bug) message")
        async def report(self, ctx, *, arg):
                thedevkiller = await self.bot.get_user_info(436105272310759426)
                await thedevkiller.send("{report}\n{auth}".format(report=arg, auth=ctx.message.author.name))

        # Convertir
        @commands.command(aliases=["convertir"], brief="Convertir deux unités", usage="(convertisseur|convert) unite1 unite2 text")
        async def convert(self, ctx, unite1, unite2, *, chaine):

                if unite1 == "ascii" and unite2 == "base64":
                        encode = base64.b64encode(str.encode(chaine))
                        await ctx.send(encode.decode())
                elif unite1 == "base64" and unite2 == "ascii":
                        decode = base64.b64decode(str.encode(chaine))
                        await ctx.send(decode.decode().capitalize())
                elif unite1 == "ascii" and unite2 == "bin":
                        encode = ' '.join(format(ord(x), 'b') for x in chaine)
                        await ctx.send(encode)
                elif unite1 == "bin" and unite2 == "ascii":
                        chaine = int(chaine, 2)
                        chaine.to_bytes((chaine.bit_length() + 7) // 8, "big").decode("utf-8", "surogatepass") or "\0"
                        msg = ""
                        for elements in chaine:
                                for element in elements[::2]:      
                                        msg += chr(element)

                else:
                        await ctx.send("Désolé mais je ne connais pas ces unités :confused:")

        # Traduire
        @commands.command(aliases=["traduire"], usage="(traduire|translate) (sourceLang|auto) targetLang string")
        async def translate(self, ctx, ls, lc, *, cs):

                # URL
                url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + ls + "&tl=" + lc + "&dt=t&q=" + cs
                
                # Requête
                cc = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}).json()[0][0][0]
                
                await ctx.send(embed=discord.Embed(title="Traduction", description="{ls}: {cs}\n{lc}: {cc}".format(ls=ls.capitalize(), cs=cs.capitalize(), lc=lc.capitalize(), cc=cc.capitalize()), color=0x225bff))

        # QR
        @commands.command(aliases=["qr"], brief="Générateur de QR code", usage="(qr|qrcode) \"chaine\", la chaine doit être entre guillemets si il y a des espaces")
        async def qrcode(self, ctx, chaine):

                # QR
                self.qr.add_data(chaine)
                self.qr.make(fit=True)
                img = self.qr.make_image(fill_color="black", back_color="white")
                img.save("qr.png")

                await ctx.send(file=discord.File("qr.png"))
                await ctx.send(chaine)
                os.remove("qr.png")

        # OCR
        @commands.command(brief="Prend le texte d'une image", usage="ocr en commentaire à l'envoi d'une image")
        async def ocr(self, ctx):

                # Image
                url = ctx.message.attachments[0].url
                image = requests.Session().get(url).content
                fichier = ctx.message.attachments[0].filename
                with open(fichier, "wb") as ocrimage:
                        ocrimage.write(image)

                # OCR
                texte = pytesseract.image_to_string(Image.open(fichier))

                await ctx.send(texte)
                os.remove(fichier)

        # TTS
        @commands.command(brief="Synthèse vocale", usage="tts \"chaine\", la chaine doit être entre guillemets si il y a des espaces")
        async def tts(self, ctx, chaine):

            # Fichier
            reponse = requests.get("https://tts.readspeaker.com/a/speak?key={token}&lang=fr_ca&voice=leo&text={chaine}".format(token=secrets["tts"], chaine=chaine)).content
            if reponse.decode().strip() == "ERROR: Needed credits exceeds available amount.":
                await ctx.send(getmsg(ctx, "nottscredits"))
            with open("tts.mp3", "wb") as fichier:
                fichier.write(mp3)
            await ctx.send(file=discord.File("tts.mp3"))

        # Dilemme
        @commands.command(aliases=["dilemme"], usage="(dilem|dilemme) \"choice1\"")
        async def dilem(self, ctx, *args):
            liste = [*args]
            await ctx.send(liste)
            choix = random.choices(liste)
            await ctx.send(choix)

def setup(bot):
        bot.add_cog(Tools(bot))
