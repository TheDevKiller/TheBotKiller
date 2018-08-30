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

#############
# Fonctions #
#############

# Obtenir une traduction
def getmsg(ctx, txt):

    # Ouvrir le fichier de traductions
    with open("trads.json", "r") as fichier:
        trad = json.loads(fichier.read())

    return trad[config[str(ctx.message.guild.id)]["lang"]][txt]


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
                self.p4 = False
                self.jTour = None
                self.jJaune = None
                self.jRouge = None
                self.grillep4 = None
                self.gris = (0, 0, 0)
                self.jaune = (0, 0, 0)
                self.rouge = (0, 0, 0)
                self.im = None
                self.draw = None
                self.shifumi = False
                self.joueurShifumi = 1
        
        # MRAW
        @commands.command(usage="mraw")
        async def mraw(self, ctx):
            await ctx.send(":regional_indicator_m: :regional_indicator_r: :regional_indicator_a: :regional_indicator_w: ")

        # Kop1
        @commands.command(name="kop1", usage="kop1")
        async def kop(self, ctx):
            await ctx.send(":regional_indicator_k: :regional_indicator_o: :regional_indicator_p: :one:")

        # <3
        @commands.command(name="heart", usage=":heart:")
        async def heart(self, ctx):
            await ctx.send(":heart:")

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
        @commands.command(usage="shifumi")
        async def shifumi(self, ctx):

                # Partie de Shifumi en cours
                self.shifumi = True

                # Joueur
                self.joueurShifumi = ctx.message.author.id

                # Message joue, à modifier
                messageJoue = await ctx.send(embed=discord.Embed(title="Shifumi", description="Joue :wink:", color=0xff7400))

                # Réactions
                await messageJoue.add_reaction("🌑")
                await messageJoue.add_reaction("📄")
                await messageJoue.add_reaction("✂")

                # Vérif' des réaction
                reactionsValides = ["🌑", "📄", "✂"]
                
                # Réactions Invalides
                while reaction[0].emoji not in reactionsValides:
                        await ctx.send("Réagis avec pierre, feuille ou ciseaux :wink:")
                        reaction = await bot.wait_for("reaction_add", check=lambda r, u: u.id == ctx.message.author.id)

                # Définition du jeu du joueur
                if reaction[0].emoji == "🌑":
                        jeuJoueur = "pierre :new_moon:"
                elif reaction[0].emoji == "📄":
                        jeuJoueur = "feuille :page_facing_up:"
                elif reaction[0].emoji == "✂":
                        jeuJoueur = "ciseaux :scissors:"

                # Jeu du bot
                elements = ["pierre :new_moon:", "feuille :page_facing_up:", "ciseaux :scissors:"]
                elementBot = random.choice(elements)

                # Possibilités pour voir les gagnants
                jeux = \
                {"pierre :new_moon:": ["ciseaux :scissors:"],
                "ciseaux :scissors:": ["feuille :page_facing_up:"],
                "feuille :page_facing_up:": ["pierre :new_moon:"]}

                # Check de qui a gagné
                if jeuJoueur == elementBot:
                        resultat = "Égalité :neutral_face:"
                elif elementBot in jeux[jeuJoueur]:
                        resultat = "T'as gagné :frowning:"
                else:
                        resultat = "T'as perdu :smiley:"

                # Édition du message
                await messageJoue.edit(embed=discord.Embed(title="Résultat du Shifumi entre " + ctx.message.author.name + " et </TheBotKiller>", description="** **\n**Tu as joué: **\n\n" + jeuJoueur.capitalize() + "\n\n**J'ai joué: **\n\n" + elementBot.capitalize() + "\n\n**Résultat: **\n\n" + resultat, color=0xff7400))

                # Deuxième check de qui a gagné pour la variable gagant
                if resultat == "Égalité :neutral_face:":
                        gagnant = "Aucun"
                elif resultat == "T'as gagné :frowning:":
                        gagnant = ctx.message.author.name
                else:
                        gagnant = "</TheBotKiller>"

                jeuJoueur = jeuJoueur.split(" ")[0]
                elementBot = elementBot.split(" ")[0]

        # Dis
        @commands.command(aliases=["dis"], usage="(dis|say) message")
        async def say(self, ctx, *, arg):
                await ctx.send(arg)

        # POM
        @commands.command(aliases=["plusoumoins", "+-", "+ou+"], usage="(+-|+ou-|plusoumoins|pom) <min> <max>")
        async def pom(self, ctx, pmin, pmax):

                # Globales
                global joueurPom
                global minpom
                global maxpom
                global nbre
                global pomchan
                global essais
                global pom

                # Variables
                minpom = pmin
                maxpom = pmax
                joueurPom = ctx.message.author

                # Check si le max et min doivent être inversés
                if(minpom > maxpom):
                        minpom, maxpom = maxpom, minpom

                await ctx.send("Devine à quel nombre je pense entre {} et {}".format(minpom, maxpom))

                # Nombre du bot & autres variables
                nbre = random.randint(int(minpom), int(maxpom))
                pomchan = ctx.message.channel
                pom = True
                essais = 1

        # P4
        @commands.command(aliases=["c4", "connect4", "puissance4"], name="p4", usage="p4 mention")
        async def _p4(self, ctx, arg):

            # Partie en cours
            self.p4 = True

            # Dessin
            self.im = Image.open("p4.png")
            self.draw = ImageDraw.Draw(self.im, "RGBA")
            self.draw.rectangle([(0, 0), (355, 348)], (58, 53, 155))
            self.draw.rectangle([(0, 306), (355, 348)], (0, 0, 0, 30))
            
            # Police (Ubuntu)
            font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf", 34)

            # Joueurs
            self.jJaune = ctx.message.author
            self.jRouge = await self.bot.get_user_info(int(arg.replace("<", "").replace(">", "").replace("@", "").replace("!", "")))

            # Joueur qui doit commencer
            self.jTour = random.choice([self.jJaune, self.jRouge])
    
            await ctx.send("C'est à %s de commencer"%self.jTour.mention)

            # Couleurs
            self.jaune = (241, 196, 15)
            self.rouge = (231, 76, 60)
            self.gris = (58, 53, 155, 0)

            # Grille
            self.grillep4 = \
                    [[self.gris, self.gris, self.gris, self.gris, self.gris, self.gris],
                    [self.gris, self.gris, self.gris, self.gris, self.gris, self.gris],
                    [self.gris, self.gris, self.gris, self.gris, self.gris, self.gris],
                    [self.gris, self.gris, self.gris, self.gris, self.gris, self.gris],
                    [self.gris, self.gris, self.gris, self.gris, self.gris, self.gris],
                    [self.gris, self.gris, self.gris, self.gris, self.gris, self.gris],
                    [self.gris, self.gris, self.gris, self.gris, self.gris, self.gris]]

            # Dessin de la grille
            for coindex, colonne in enumerate(self.grillep4):
                coindex *= 50
                for caindex, case in enumerate(colonne):
                    caindex *= 50
                    self.draw.ellipse([(coindex+5, caindex+5), (coindex+50, caindex+50)], case)

            # Dessin des nombres en bas de la grille
            for index, n in enumerate(range(1, 8)):
                index *= 50
                self.draw.text((index + 20, 305), str(n), "white", font)

            # Sauvegarde & Envoi de l'image
            self.im.save("p4.png")
            await ctx.send(file=discord.File("p4.png"))

        # Martine
        @commands.command(usage="martine imageName text")
        async def martine(self, ctx, image, *, texte):

            image = image.lower()

            imageList = ['ecole', 'surprise', 'lanterne', 'train', 'camping', 'menage', 'ferme', 'zoo', 'fantome', 'contes', 'ours', 'rentree', 'princesse', 'maman', 'voyage', 'accident', 'noel', 'demenage', 'avion', 'theatre', 'mongolfiere']

            if image not in imageList:
                await ctx.send("Liste des images disponibles:\n\n- %s"%"\n- ".join(imageList))

            else:
                for i, e in enumerate(imageList):
                    if e == image:
                        imageNbre = i

                source = requests.get("http://www.retourdemartine.free.fr/create2.php?t=%s&m=%s"%(texte, imageNbre+1), headers={"User-Agent": "Un gentil bot discord"}).content

                soup = BeautifulSoup(source, "html.parser")

                imgUrl = "http://www.retourdemartine.free.fr/" + soup.find("img", class_="blackborder")["src"]

                await ctx.send(imgUrl)

        # Pi
        @commands.command(usage="pi number")
        async def pi(self, ctx, nbre):

            pi = "141592653589"

            if nbre in pi:
                await ctx.send("Votre nombre est dans les 12 premières décimales de pi")

            else:
                await ctx.send("Votre nombre n'est pas dans les 12 premières décimales de pi")

        # Réactions
        async def on_reaction_add(self, reaction, user):
            
            reactionValides = [":page_facing_up:" ":new_moon:" ":scissors:"]

            if self.shifumi == True:
                #if reaction.message.author.id == self.shifumijoueur:
                    #if reaction.name in reactionValides:
                self.jeuJoueurShifumi = reaction.name
                print("JEUJOUEUR: %s"%self.jeuJoueurShifumi)


        # Messages
        async def on_message(self, message):
       
            # Essais du POM
            global essais
            
            # POM    
            if pom == True and message.author == joueurPom and message.channel == pomchan:
                
                # Nombre du joueur
                nbreJoueur = int(message.content)
                
                # Vérifications
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
                    
                    # Fin de la partie
                    plusoumoins = False
        
            # P4
            elif self.p4 == True and message.author.id == self.jTour.id:

                # Vérification si le message est un nombre entre 1 & 8 (largeur de la grille)
                for e in range(1, 8):
                    if message.content.strip() == str(e):
                        
                        # Vérification des cases de bas en haut une par une pour jouer
                        for index, case in enumerate(self.grillep4[int(message.content) - 1]):
                            
                            # Vérification de quel joueur joue
                            if case == self.gris:
                                if self.jTour == self.jJaune:
                                    self.grillep4[int(message.content) - 1][index] = self.jaune
                                    break
                                elif self.jTour == self.jRouge:
                                    self.grillep4[int(message.content) - 1][index] = self.rouge
                                    break

                        # Inverse la grille
                        for element in self.grillep4:
                            element.reverse()

                        # Dessin de la grille colonne par colonne
                        for coindex, colonne in enumerate(self.grillep4):
                            coindex *= 50
                            for caindex, case in enumerate(colonne):
                                caindex *= 50
                                self.draw.ellipse([(coindex+5, caindex+5), (coindex+50, caindex+50)], case)

                        # Sauvegarde de l'image
                        self.im.save("p4.png")

                        # Changement de tour
                        if self.jTour == self.jRouge:
                            self.jTour = self.jJaune
                        elif self.jTour == self.jJaune:
                            self.jTour = self.jRouge

                        # Vérifications des colonnes
                        for coindex, colonne in enumerate(self.grillep4):
                            for caindex, case in enumerate(colonne):
                                try:
                                    if self.grillep4[coindex][caindex:caindex+4].count(self.jaune) == 4 or self.grillep4[coindex][caindex:caindex+4].count(self.rouge) == 4:
                                        if self.grillep4[coindex][caindex] == self.jaune:
                                            if self.p4 == True:
                                                await message.channel.send("%s, tu as gagné, bien joué !"%self.jJaune.mention, file=discord.File("p4.png"))
                                            self.p4 = False
                                        elif self.grillep4[coindex][caindex] == self.rouge:
                                            if self.p4 == True:
                                                await message.channel.send("%s, tu as gagné, bien joué !"%self.jRouge.mention, file=discord.File("p4.png"))
                                            self.p4 = False
                                except:
                                    pass

                        # Vérification des lignes
                        ligne = []
                        for coindex, colonne in enumerate(self.grillep4):
                            for caindex, case in enumerate(colonne):
                                for coindex, colonne in enumerate(self.grillep4):
                                    ligne.append(self.grillep4[coindex][caindex])
                                for index, case in enumerate(ligne):
                                    if ligne[index:index+4].count(self.jaune) == 4 or ligne[index:index+4].count(self.rouge) == 4:
                                        if ligne[index] == self.rouge:
                                            if self.p4 == True: 
                                                await message.channel.send("%s, tu as gagné, bien joué !"%self.jRouge.mention)
                                            self.p4 = False
                                            break
                                        elif ligne[index] == self.jaune:
                                            if self.p4 == True: 
                                                await message.channel.send("%s, tu as gagné, bien joué !"%self.jRouge.mention)
                                            self.p4 = False
                                            break                                

                        # Vérification des diagonales
                        diagonales = []
                        a = np.array(self.grillep4)
                        diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
                        diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
                        for n in diags:
                            diagonales.append(n.tolist())
                        for dindex, d in enumerate(diagonales):
                            for cindex, c in enumerate(d):
                                try:
                                    if diagonales[dindex][cindex:cindex+4].count(self.jaune) == 4 or diagonales[dindex][cindex:cindex+4].count(self.rouge) == 4:
                                        print("le premier if passe")
                                        if diagonales[dindex][cindex] == self.rouge:
                                            if self.p4 == True: 
                                                await message.channel.send("%s, tu as gagné, bien joué !"%self.jRouge.mention, file=discord.File("p4.png"))
                                            self.p4 = False
                                            break
                                        elif diagonales[dindex][cindex] == self.jaune:
                                            print("le deuxième if passe")
                                            if self.p4 == True: 
                                                await message.channel.send("%s, tu as gagné, bien joué !"%self.jRouge.mention, file=discord.File("p4.png"))
                                            self.p4 = False
                                            break
                                except IndexError:
                                    pass

                        if self.p4 == True:
                            await message.channel.send("À toi, %s"%self.jTour.mention, file=discord.File("p4.png"))

                        # Inversement de la grille
                        for element in self.grillep4:
                            element.reverse()



def setup(bot):
        bot.add_cog(Fun(bot)) 