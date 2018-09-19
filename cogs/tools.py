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

    try:
        return trad[config[str(ctx.message.guild.id)]["lang"]][txt]

    except:
        return trad["fr"][txt]

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

        # Clearme
        @commands.command(usage="clearme")
        async def clearme(self, ctx):
            async for message in ctx.history(limit=100, before=ctx.message):
                if message.author == ctx.guild.me:
                    await message.delete()

        @commands.command(usage="clear <limit>")
        async def clear(self, ctx, limit):
            thedevkiller = await self.bot.get_user_info(436105272310759426)
            if ctx.message.author == thedevkiller:
                async for message in ctx.history(limit=int(limit)+1):
                    await message.delete()
            else:
                await ctx.send(f"Nique ta mère")

        # Todo
        @commands.command(usage="todo (add|remove|modify|view) [number] text")
        async def todo(self, ctx, action="view", *, text=""):
            # Add a task
            if action == "add":
                # Capitalize the task
                text = text.capitalize()
                # Open the todo's file
                with open("todo.json", "r") as file:
                    dico = json.loads(file.read())
                # If the user has a To-Do list, add the task to it
                if str(ctx.message.author.id) in dico:
                    # Verify if the list is valid
                    if isinstance(dico[str(ctx.message.author.id)], list):
                        # Add the task to the list
                        dico[str(ctx.message.author.id)].append(text)
                    # If the task isn't valid
                    else:
                        # Create the list
                        dico[str(ctx.message.author.id)] = []
                        # Add the task to the list
                        dico[str(ctx.message.author.id)].append(text)
                    await ctx.send(getmsg(ctx, "Task successfully added"))
                # If the user hasn't a To-Do list
                else:
                    # Create the user's To-Do list
                    dico[str(ctx.message.author.id)] = []
                    # Add the task to the list
                    dico[str(ctx.message.author.id)].append(text)
                # Write the To-Do list's JSON
                with open("todo.json", "w") as file:
                    file.write(json.dumps(dico, indent=4))
            # View the user's To-Do list
            elif action == "view":
                # Open the To-Do list's file
                with open("todo.json", "r") as file:
                    dico = json.loads(file.read())
                # If the user has a To-Do list and it's not empty
                if str(ctx.message.author.id) in dico and dico[str(ctx.message.author.id)] != []:
                    # Create the formatted list and the embed
                    description = ""
                    for i, e in enumerate(dico[str(ctx.message.author.id)]):
                        description += f"{i+1}. {e}\n"
                    em = discord.Embed(title=getmsg(ctx, "Your To-Do list"), description=description, color=0xff6600)
                    # Send the embed
                    await ctx.send(embed=em)
                # If the user hasn't got a To
                else:
                    await ctx.send(getmsg(ctx, "You have no To-Do list"))
            # Remove a task from the To-Do list
            elif action == "remove":
                # Get task's index in list
                nbre = int(text.split(" ")[0])
                # Open the To-Do list's file
                with open("todo.json", "r") as file:
                    dico = json.loads(file.read())
                # Delete the task from the list
                del dico[str(ctx.message.author.id)][nbre - 1]
                # Write the changes
                with open("todo.json", "w") as file:
                    file.write(json.dumps(dico, indent=4))
                await ctx.send(getmsg(ctx, "Task successfully removed"))
            # Modify a task
            elif action == "modify":
                # Open the To-Do list's file
                with open("todo.json", "r") as file:
                    dico = json.loads(file.read())
                # Get task's index in list
                nbre = int(text.split(" ")[0])
                # Get the new text
                texte = ""
                for e in text.split(" ")[1:]:
                    texte += e + " "
                # Replace the element by the text
                dico[str(ctx.message.author.id)][nbre - 1] = texte
                # Write all changes in the file
                with open("todo.json", "w") as file:
                    file.write(json.dumps(dico, indent=4))
                await ctx.send(getmsg(ctx, "Task successfully modified"))

        # Report
        @commands.command(aliases=["bug"], brief="Signaler un bug", usage="(report|bug) message")
        async def report(self, ctx, *, arg):
                thedevkiller = await self.bot.get_user_info(436105272310759426)
                await thedevkiller.send(f"{arg}\n{ctx.message.author.name}")

        # Traduire
        @commands.command(aliases=["traduire"], usage="(traduire|translate) (sourceLang|auto) targetLang string")
        async def translate(self, ctx, ls, lc, *, cs):

                # URL
                url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + ls + "&tl=" + lc + "&dt=t&q=" + cs
                
                # Requête
                cc = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}).json()[0][0][0]
                
                await ctx.send(embed=discord.Embed(title="Traduction", description=f"{ls.capitalize()}: {cs.capitalize()}\n{lc.capitalize()}: {cc.capitalize()}", color=0x225bff))

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
            reponse = requests.get(f"https://tts.readspeaker.com/a/speak?key={secrets['tts']}&lang=fr_ca&voice=leo&text={chaine}").content
            if reponse.decode().strip() == "ERROR: Needed credits exceeds available amount.":
                await ctx.send(getmsg(ctx, "nottscredits"))
            else:
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
