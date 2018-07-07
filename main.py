#!/usr/bin/python3
#coding: utf8

# Imports

import discord
import asyncio
import random

# /Imports

# Token

with open("token.txt", "r") as tokenFile:
	token = tokenFile.read()

# /Token

# Variables

global prefixe
prefixe = "&"

commandes = \
"""
`help`: Affiche cette page d'aide
`code`: Envoie mon lien Github
`shifumi <élément>`: Joue avec moi au shifumi !
`+- <min> <max>`: Joue avec moi au plus ou moins !
"""

# / Variables

# Connexion

print("Chargement de </TheBotKiller> avec le token", token)

client = discord.Client()

plusoumoins = False

@client.event
async def on_ready():
	global thedevkiller
	thedevkiller = await client.get_user_info("436105272310759426")
	print("</TheBotKiller> est prêt à discuter avec les utilisateurs et à jouer avec eux !")
	await client.change_presence(game=discord.Game(name="&help (ou prefixe + help)"))

# /Connexion

# Fonctions

def messageGrille(grilleListe):
			
	grille = "\n" 
	for index, elements in enumerate(grilleListe):
		if index != 0:
			grille += "\n**－－＋－－＋－－**\n"
		for index, elements2 in enumerate(elements):
			grille += elements2
			if index != 2:
				grille += " ｜ "

	return grille

# /Fonctions

@client.event
async def on_message(message): # Dès qu'il y a un message

	global plusoumoins

	if client.user.mentioned_in(message) and message.author == thedevkiller and str(message.content.split(" ")[1]) == "préfixe": # Changement du préfixe
		global prefixe
		prefixe = str(message.content.split(" ")[2])
		await client.send_message(message.channel, "Mon préfixe est désormais" + " " + prefixe)
		print("Le préfixe de </TheBotKiller> est désormais " + prefixe)

	elif message.content.startswith(prefixe + "code"): # Envoie le lien Github
		await client.send_message(message.channel, "https://github.com/TheDevKiller/TheBotKiller")

	elif message.content.startswith(prefixe + "shifumi"): # Commence une partie de Shifumi
		elements = ["pierre", "feuille", "ciseaux"]
		jeuJoueur = message.content.split(" ")[1].lower()
		jeuBot = random.choice(elements)

		if jeuJoueur == jeuBot:                                 
			resultat = "Égalité"                                
		elif jeuJoueur == "pierre" and jeuBot == "feuille":     
			resultat = "T'as perdu"
		elif jeuJoueur == "pierre" and jeuBot == "ciseaux":
			resultat = "T'as gagné"                                # La deuxième personne du singulier
		elif jeuJoueur == "feuille" and jeuBot == "pierre":        # c'est le joueur
			resultat = "T'as gagné"
		elif jeuJoueur == "ciseaux" and jeuBot == "pierre":
			resultat = "T'as perdu"
		elif jeuJoueur == "feuille" and jeuBot == "ciseaux":
			resultat = "T'as perdu"
		elif jeuJoueur == "ciseaux" and jeuBot == "feuille":
			resultat = "T'as gagné"
		else:
			await client.send_message(message.channel, "Entre un élément valide la prochaine fois s'il te plaît :wink:")

		await client.send_message(message.channel, embed=discord.Embed(title="Résultat du Shifumi entre " + message.author.name + " et </TheBotKiller>", description="**Tu as joué: **\n" + jeuJoueur.capitalize() + "\n\n**J'ai joué: **\n" + jeuBot.capitalize() + "\n\n**Résultat: **\n" + resultat, color=0x00ff00))

	elif message.content.startswith(prefixe + "help"):
		await client.send_message(message.channel, embed=discord.Embed(title="Liste des commandes disponibles", description=commandes, color=0x0055FE))

	elif message.content.startswith(prefixe + "+-"):
		try:
			min = int(message.content.split(" ")[1])
			max = int(message.content.split(" ")[2])
			await client.send_message(message.channel, "Devine à quel nombre je pense entre " + str(min) + " et " + str(max))
			global nombre
			nombre = random.randint(min, max)
			global plusoumoinschan 
			plusoumoinschan = message.channel
			plusoumoins = True
			global essais
			essais = 1
		except Exception as ex:
			await client.send_message(message.channel, "```python\n" + str(ex) + "\n```")
			await client.send_message(message.channel, "Entre des nombres valides s'il te plaît :wink:")

	elif plusoumoins == True and message.author != client.user and message.channel == plusoumoinschan:
		try:
			nombreJoueur = int(message.content)
			if nombreJoueur < nombre:
				await client.send_message(message.channel, "C'est plus !")
				essais += 1
			elif nombreJoueur > nombre:
				await client.send_message(message.channel, "C'est moins !")
				essais += 1
			elif nombreJoueur == nombre:
				if essais <= 1:
					await client.send_message(message.channel, "C'est ça, bien joué " + message.author.mention + " ! Tu as réussi en " + str(essais) + " essai")
				else:
					await client.send_message(message.channel, "C'est ça, bien joué " + message.author.mention + " ! Tu as réussi en " + str(essais) + " essais")

				plusoumoins = False
			else:
				await client.send_message(message.channel, "Entre des nombres valides s'il te plaît :wink:")
		except Exception as ex:
			await client.send_message(message.channel, "```python\n" + str(ex) + "\n```")
			await client.send_message(message.channel, "Entre des nombres valides s'il te plaît :wink:")

	elif message.content.startswith(prefixe + "dilemme"):

		try:
			premierChoixListe = message.content.split(",")[0]
			premierChoixListe = premierChoixListe.split(" ")
			del premierChoixListe[0]
			premierChoix = ""
			deuxiemeChoix = ""
			for elements in premierChoixListe:
				premierChoix += elements + " "
			deuxiemeChoixListe = message.content.split(",")[1].strip()
			for elements in deuxiemeChoixListe:
				deuxiemeChoix += elements
			premierChoix = premierChoix.strip()
			listeChoix = [premierChoix, deuxiemeChoix]
			choix = str(random.choice(listeChoix))
			await client.send_message(message.channel, "Je dirais " + choix.lower())

		except Exception as ex:
			await client.send_message(message.channel,"```\n" + str(ex) + "\n```")

	elif message.content.startswith(prefixe + "morpion"):

		try:

			enPartie = True

			symboles = [":x:", ":o:"]

			symboleJoueur = random.choice(symboles)

			grilleListe = [[":one:", ":two:", ":three:"],  [":four:", ":five:", ":six:"], [":seven:", ":eight:", ":nine:"]] # Création de la grille vide

			await client.send_message(message.channel, "Commence, tu joue avec les " + symboleJoueur + " !")
			messageEnvoyeGrille = await client.send_message(message.channel, embed=discord.Embed(title="Morpion", description=messageGrille(grilleListe)))

			await client.add_reaction(messageEnvoyeGrille, "1⃣")
			await client.add_reaction(messageEnvoyeGrille, "2⃣")
			await client.add_reaction(messageEnvoyeGrille, "3⃣")
			await client.add_reaction(messageEnvoyeGrille, "4⃣")
			await client.add_reaction(messageEnvoyeGrille, "5⃣")
			await client.add_reaction(messageEnvoyeGrille, "6⃣")
			await client.add_reaction(messageEnvoyeGrille, "7⃣")
			await client.add_reaction(messageEnvoyeGrille, "8⃣")
			await client.add_reaction(messageEnvoyeGrille, "9⃣")

			while enPartie == True:

				reaction = await client.wait_for_reaction(user=message.author)

				casesInterdites = [0]

				if reaction.reaction.emoji == "1⃣":
					grilleListe[0][0] = symboleJoueur
					casesInterdites.append(1)
				elif reaction.reaction.emoji == "⃣":
					grilleListe[0][1] = symboleJoueur
					casesInterdites.append(2)
				elif reaction.reaction.emoji == "3⃣":
					grilleListe[0][2] = symboleJoueur
					casesInterdites.append(3)
				elif reaction.reaction.emoji == "4⃣":
					grilleListe[1][0] = symboleJoueur
					casesInterdites.append(4)
				elif reaction.reaction.emoji == "5⃣":
					grilleListe[1][1] = symboleJoueur
					casesInterdites.append(5)
				elif reaction.reaction.emoji == "6⃣":
					grilleListe[1][2] = symboleJoueur
					casesInterdites.append(6)
				elif reaction.reaction.emoji == "7⃣":
					grilleListe[2][0] = symboleJoueur
					casesInterdites.append(7)
				elif reaction.reaction.emoji == "8⃣":
					grilleListe[2][1] = symboleJoueur
					casesInterdites.append(8)
				elif reaction.reaction.emoji == "9⃣":
					grilleListe[2][2] = symboleJoueur
					casesInterdites.append(9)
				else:
					await client.send_message(message.channel, "Réagis avec un nombre valide entre 1 et 9 s'il te plaît :wink:")
				
				choixCaseBot = random.randint(1, 9)

				if symboleJoueur == ":x:":
					symboleBot = ":o:"
				elif symboleJoueur == ":o:":
					symboleBot = ":x:"
				else:
					symboleBot = "Aucun symbole"

				if grilleListe[0][0] == symboleBot and grilleListe[0][1] == ":two:":
					grilleListe[0][1] = symboleBot
				elif grilleListe[0][0] == symboleBot and grilleListe[1][0] == ":four:":
					grilleListe[1][0] = symboleBot
				elif grilleListe[0][0] == symboleBot and grilleList[1][1] == ":five:":
					grilleListe[1][1] = symboleBot
				elif grilleListe[0][1] == symboleBot and grilleListe[0][0] == ":one:":
					grilleListe[0][0] = symboleBot
				elif grilleListe[0][1] == symboleBot and grilleListe[1][0] == ":four:":
					grilleListe[1][0] = symboleBot
				elif grilleListe[0][1] == symboleBot and grilleListe[1][1] == ":five:":
					grilleListe[1][1] = symboleBot
				elif grilleListe[0][1] == symboleBot and grilleListe[1][2] == ":six:":
					grilleListe[1][2] = symboleBot
				elif grilleListe[0][1] == symboleBot and grilleListe[0][2] == ":three:":
					grilleListe[0][2] = symboleBot
				elif grilleListe[0][2] == symboleBot and grilleListe[0][1] == ":two:":
					grilleListe[0][1] = symboleBot
				elif grilleListe[0][2] == symboleBot and grilleListe[1][1] == ":five:":
					grilleListe[1][1] = symboleBot
				elif grilleListe[0][2] == symboleBot and grilleListe[1][2] == ":six:":
					grilleListe[1][2] = symboleBot
				elif grilleListe[1][0] == symboleBot and grilleListe[0][0] == ":one:":
					grilleListe[0][0] = symboleBot
				elif grilleListe[1][0] == symboleBot and grilleListe[0][1] == ":two:":
					grilleListe[0][1] = symboleBot

##                               0       1       2
##                          0 -[0|0]- -[0|1]- -[0|2]-		[1] [2] [3]
##
##                          1  [1|0]   [1|1]   [1|2]		[4] [5] [6]
##
##                          2  [2|0]   [2|1]   [2|2]		[7] [8] [9]
##

				elif symboleBot not in grilleListe:

					if choixCaseBot == 1:
						grilleListe[0][0] = symboleBot
						casesInterdites.append(1)
					elif choixCaseBot == 2:
						grilleListe[0][1] = symboleBot
						casesInterdites.append(2)
					elif choixCaseBot == 3:
						grilleListe[0][2] = symboleBot
						casesInterdites.append(3)
					elif choixCaseBot == 4:
						grilleListe[1][0] = symboleBot
						casesInterdites.append(4)
					elif choixCaseBot == 5:
						grilleListe[1][1] = symboleBot
						casesInterdites.append(5)
					elif choixCaseBot == 6:
						grilleListe[1][2] = symboleBot
						casesInterdites.append(6)
					elif choixCaseBot == 7:
						grilleListe[2][0] = symboleBot
						casesInterdites.append(7)
					elif choixCaseBot == 8:
						grilleListe[2][1] = symboleBot
						casesInterdites.append(8)
					elif choixCaseBot == 9:
						grilleListe[2][2] = symboleBot
						casesInterdites.append(9)



				await client.edit_message(messageEnvoyeGrille, embed=discord.Embed(title="Morpion", description=messageGrille(grilleListe)))

		except Exception as ex:

			await client.send_message(message.channel, "```python\n" + str(ex) + "\n```")

client.run(token)