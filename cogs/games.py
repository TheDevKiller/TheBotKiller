###########
# Imports #
###########

import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import random

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

class Games:

    def __init__(self, bot):

        self.bot = bot

        bot.p4 = False

    # Batons
    @commands.command(usage="sticks <mention>", aliases=["batons"])
    async def sticks(self, ctx, j2:discord.Member):
        batons = 30
        j1 = ctx.message.author
        j2 = j2
        tour = j1  
        while batons > 0:
            n = 0

            await ctx.send(f"{batons*'|'}")
            await ctx.send(f"{tour.name}, prend un, deux ou trois bâtons")

            def check(m):
                return m.author == tour

            msg = await self.bot.wait_for("message", check=check)

            try: 
                n = int(msg.content)

            except:
                await ctx.send("Entre un nombre valide !")

            if n not in list(range(1, 4)):
                await ctx.send("Entre un nombre entre 1 et 3 !")

            else:
                gagnant = tour
                batons -= n

                if tour == j1:
                    tour = j2
                elif tour == j2:
                    tour = j1
                else:
                    print("Oups, un problème est survenu lors du changement des tours")

        await ctx.send(f"{gagnant.name} a gagné")

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

        await ctx.send(f"Devine à quel nombre je pense entre {minpom} et {maxpom}")

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
        self.im = Image.open("tmp/p4.png")
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

        await ctx.send(f"C'est à {self.jTour.mention} de commencer")

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
        self.im.save("tmp/p4.png")
        await ctx.send(file=discord.File("tmp/p4.png"))

    ############
    # Messages #
    ############

    async def on_messages(message):

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
                    await message.channel.send(f"C'est ça, bien joué {message.author.mention} ! Tu as réussi en {essais} essais")
                else:
                    await message.channel.send(f"C'est ça, bien joué {message.author.mention} ! Tu as réussi en {essais} essais")
                
                # Fin de la partie
                plusoumoins = False

	   # P4
        elif bot.p4 == True and message.author.id == self.jTour.id:

            # Vérification de si le message est un nombre entre 1 & 8 (largeur de la grille)
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
                    self.im.save("tmp/p4.png")

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
                                            await message.channel.send(f"{self.jJaune.mention}, tu as gagné, bien joué !", file=discord.File("tmp/p4.png"))
                                        self.p4 = False
                                    elif self.grillep4[coindex][caindex] == self.rouge:
                                        if self.p4 == True:
                                            await message.channel.send(f"{self.jRouge.mention}, tu as gagné, bien joué !", file=discord.File("tmp/p4.png"))
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
                                            await message.channel.send(f"{self.jRouge.mention}, tu as gagné, bien joué !")
                                        self.p4 = False
                                        break
                                    elif ligne[index] == self.jaune:
                                        if self.p4 == True: 
                                            await message.channel.send(f"{self.jRouge.mention}, tu as gagné, bien joué !")
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
                                            await message.channel.send(f"{self.jRouge.mention}, tu as gagné, bien joué !", file=discord.File("tmp/p4.png"))
                                        self.p4 = False
                                        break
                                    elif diagonales[dindex][cindex] == self.jaune:
                                        print("le deuxième if passe")
                                        if self.p4 == True: 
                                            await message.channel.send(f"{self.jRouge.mention}, tu as gagné, bien joué !", file=discord.File("tmp/p4.png"))
                                        self.p4 = False
                                        break
                            except IndexError:
                                pass

                    if self.p4 == True:
                        await message.channel.send(f"À toi, {self.jTour.mention}", file=discord.File("tmp/p4.png"))

                    # Inversement de la grille
                    for element in self.grillep4:
                        element.reverse()

def setup(bot):
	bot.add_cog(Games(bot))
