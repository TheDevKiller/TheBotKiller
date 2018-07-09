#!/usr/bin/python3
#coding: utf8

# Imports

import discord
import asyncio
import random
import re

# /Imports

# Token

with open("token.txt", "r") as tokenFile:
	token = tokenFile.read()

# /Token

# Variables

commandes = \
"""
Si vous voulez, vous pouvez discuter avec moi :smiley:. Mentionnez-moi et si je ne suis pas trop occupé, je vous répondrais peut-être :wink:)

`report`: Je bug ? Je vous envoie une erreur ? Je triche ? Faites-le moi savoir grâce à cette commande avec l'erreur si il y en a une :wink:

`help`: Affiche cette page d'aide
`code`: Mon code sur Github
`shifumi <élément>`: Joue avec moi au shifumi !
`+- <min> <max>`: Joue avec moi au plus ou moins !
"""

# / Variables

# Connexion

print("Chargement de </TheBotKiller>")

client = discord.Client()

plusoumoins = False

@client.event
async def on_ready():
	global thedevkiller
	thedevkiller = await client.get_user_info("436105272310759426")
	print("</TheBotKiller> est prêt à discuter avec les utilisateurs et à jouer avec eux !\n\n")
	await client.change_presence(game=discord.Game(name="&help (ou prefixe + help)"))

# /Connexion

# Fonctions

def messageGrille(grilleListe):
			
	grille = "\n" 
	for index, elements in enumerate(grilleListe):
		if index != 0:
			grille += "\n\n"
		for index, elements2 in enumerate(elements):
			grille += elements2
			if index != 2:
				grille += "    "

	return grille

# /Fonctions

@client.event
async def on_message(message): # Dès qu'il y a un message

	global plusoumoins

	global questioncava

	try:
		questioncava
	except:
		questioncava = False

	global prefixe

	try:
		prefixe
	except:
		prefixe = "&"

		# Code
	if message.content.startswith(prefixe + "code"): # Envoie le lien Github
		await client.send_message(message.channel, "https://github.com/TheDevKiller/TheBotKiller")

		# Shifumi

	elif message.content.startswith(prefixe + "shifumi"): # Commence une partie de Shifumi

		messageJoue = await client.send_message(message.channel, embed=discord.Embed(title="Shifumi", description="Joue :wink:", color=0xff7400))

		await client.add_reaction(messageJoue, "🌑")
		await client.add_reaction(messageJoue, "📄")
		await client.add_reaction(messageJoue, "✂")

		reaction = await client.wait_for_reaction(user=message.author)

		if reaction.reaction.emoji == "🌑":
			jeuJoueur = "pierre :new_moon:"
		elif reaction.reaction.emoji == "📄":
			jeuJoueur = "feuille :page_facing_up:"
		elif reaction.reaction.emoji == "✂":
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

		await client.edit_message(messageJoue, embed=discord.Embed(title="Résultat du Shifumi entre " + message.author.name + " et </TheBotKiller>", description="** **\n**Tu as joué: **\n\n" + jeuJoueur.capitalize() + "\n\n**J'ai joué: **\n\n" + elementBot.capitalize() + "\n\n**Résultat: **\n\n" + resultat, color=0xff7400))

		# Help
	elif message.content.startswith(prefixe + "help"):
		await client.send_message(message.channel, embed=discord.Embed(title="Liste des commandes disponibles", description=commandes, color=0x0055FE))

		# Plus Ou Moins
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

			# Plus Ou Moins
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

			# Dilemme
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


			# Morpion
	elif message.content.startswith(prefixe + "morpion") or re.match(".*morpion.? " + client.user.mention + ".*", message.content.lower()) and message.author != client.user:

		try:

				# Variables
			enPartieMorpion = True

			ligneBot = 0

			symboles = [":x:", ":o:"]

			symboleJoueur = random.choice(symboles)

			leBotAGagné = False

				# Symbole Bot
			if symboleJoueur == ":x:":
				symboleBot = ":o:"
			elif symboleJoueur == ":o:":
				symboleBot = ":x:"


			grilleListe = [[":one:", ":two:", ":three:"],  [":four:", ":five:", ":six:"], [":seven:", ":eight:", ":nine:"]] # Création de la grille vide

				# Jeu
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

			casesInterdites19 = []
			casesInterditesEmo = []
			choixJoueur = None
			caseBot = 0
			ligneBot = 0
			colonneBot = 0

			print(message.author.name, "a commencé une partie de morpion")

			while enPartieMorpion == True:

				reaction = await client.wait_for_reaction(user=message.author, message=messageEnvoyeGrille)

					# Choix du joueur avec la réaction
				if reaction.reaction.emoji == "1⃣":
					choixJoueur = ":one:"
				elif reaction.reaction.emoji == "2⃣":
					choixJoueur = ":two:"
				elif reaction.reaction.emoji == "3⃣":
					choixJoueur = ":three:"
				elif reaction.reaction.emoji == "4⃣":
					choixJoueur = ":four:"
				elif reaction.reaction.emoji == "5⃣":
					choixJoueur = ":five:"
				elif reaction.reaction.emoji == "6⃣":
					choixJoueur = ":six:"
				elif reaction.reaction.emoji == "7⃣":
					choixJoueur = ":seven:"
				elif reaction.reaction.emoji == "8⃣":
					choixJoueur = ":eight:"
				elif reaction.reaction.emoji == "9⃣":
					choixJoueur = ":nine:"
				print(choixJoueur)
				print(str(casesInterditesEmo))

					# Boucle pour les cases interdites
				if choixJoueur in casesInterditesEmo:
					print(str(casesInterditesEmo))
					await client.send_message(message.channel, "Cette case est déjà prise !")
					print(message.author.name, "a essayé de jouer une case déjà prise, la choixJoueur")
					while choixJoueur in casesInterditesEmo:
						reaction = await client.wait_for_reaction(user=message.author, message=messageEnvoyeGrille)
						await client.send_message(message.channel, "Cette case est déjà prise !")
						print(message.author.name, "a essayé de jouer une case déjà prise, la",  choixJoueur)


							# Deuxième choix avec les réactions
						if reaction.reaction.emoji == "1⃣":
							choixJoueur = ":one:"
						elif reaction.reaction.emoji == "⃣":
							choixJoueur = ":two:"
						elif reaction.reaction.emoji == "3⃣":
							choixJoueur = ":three:"
						elif reaction.reaction.emoji == "4⃣":
							choixJoueur = ":four:"
						elif reaction.reaction.emoji == "5⃣":
							choixJoueur = ":five:"
						elif reaction.reaction.emoji == "6⃣":
							choixJoueur = ":six:"
						elif reaction.reaction.emoji == "7⃣":
							choixJoueur = ":seven:"
						elif reaction.reaction.emoji == "8⃣":
							choixJoueur = ":eight:"
						elif reaction.reaction.emoji == "9⃣":
							choixJoueur = ":nine:"



					# Placement du symbole du joueur
				if choixJoueur == ":one:":
					grilleListe[0][0] = symboleJoueur
					casesInterditesEmo.append(":one:")
					casesInterdites19.append(1)
				elif choixJoueur == ":two:":
					grilleListe[0][1] = symboleJoueur
					casesInterditesEmo.append(":two:")
					casesInterdites19.append(2)
				elif choixJoueur == ":three:":
					grilleListe[0][2] = symboleJoueur
					casesInterditesEmo.append(":three:")
					casesInterdites19.append(3)
				elif choixJoueur == ":four:":
					grilleListe[1][0] = symboleJoueur
					casesInterditesEmo.append(":four:")
					casesInterdites19.append(4)
				elif choixJoueur == ":five:":
					grilleListe[1][1] = symboleJoueur
					casesInterditesEmo.append(":five:")
					casesInterdites19.append(5)
				elif choixJoueur == ":six:":
					grilleListe[1][2] = symboleJoueur
					casesInterditesEmo.append(":six:")
					casesInterdites19.append(6)
				elif choixJoueur == ":seven:":
					grilleListe[2][0] = symboleJoueur
					casesInterditesEmo.append(":seven:")
					casesInterdites19.append(7)
				elif choixJoueur == ":eight:":
					grilleListe[2][1] = symboleJoueur
					casesInterditesEmo.append(":eight:")
					casesInterdites19.append(8)
				elif choixJoueur == ":nine:":
					grilleListe[2][2] = symboleJoueur
					casesInterditesEmo.append(":nine:")
					casesInterdites19.append(9)
				else:
					await client.send_message(message.channel, "Réagis avec un nombre valide entre 1 et 9 s'il te plaît :wink:")
				
					# Check si le bot a joué
				symboleBotPasDansGrilleListe = True
				for elements in grilleListe:
					for elements2 in elements:
						if symboleBot in elements2:
							symboleBotPasDansGrilleListe = False

					# Diagonales
				diagonaleGD = [grilleListe[0][0], grilleListe[1][1], grilleListe[2][2]]
				diagonaleDG = [grilleListe[0][2], grilleListe[1][1], grilleListe[2][0]]

					# Vérification de la grille pour 2 éléments côtes à côtes

					# Vérification horizontale
				for index, elements in enumerate(grilleListe):
					if elements == [r":(o|x){1}:", r":(o|x){1}:", r":.*:"]:
						colonneBot = 3
						leBotAGagné = True
						ligneBot = index
					elif elements == [r":(o|x){1}:", r":.*:", r":(o|x){1}:"]:
						colonneBot = 2
						leBotAGagné = True
						ligneBot = index
					elif elements == [r":.*:", r":(o|x){1}:", r":(o|x){1}:"]:
						colonneBot = 1
						leBotAGagné = True
						ligneBot = index
					else:
						if symboleBotPasDansGrilleListe == True:
							caseBot = random.randint(1, 9)
							if caseBot in casesInterdites19:
								while caseBot in casesInterdites19:
									caseBot = random.randint(1, 9)

					grilleListeCopieVerticale = [elements[0] for elements in grilleListe]
					grilleListeCopieVerticale.append([elements[1] for elements in grilleListe])
					grilleListeCopieVerticale.append([elements[2] for elements in grilleListe])

						# Vérification verticale
					for index, elements in enumerate(grilleListeCopieVerticale):
						if elements == [r":(o|x){1}:", r":(o|x){1}:", r":.*:"]:
							ligneBot = 2
							leBotAGagné = True
							colonneBot = index
						elif elements == [r":(o|x){1}:", r":.*:", r":(o|x){1}:"]:
							ligneBot = 1
							leBotAGagné = True
							colonneBot = index
						elif elements == [r":.*:", r":(o|x){1}:", r":(o|x){1}:"]:
							ligneBot = 0
							leBotAGagné = True
							colonneBot = index
						else:
							if symboleBotPasDansGrilleListe == True:
								caseBot = random.randint(1, 9)
								if caseBot in casesInterdites19:
									while caseBot in casesInterdites19:
										caseBot = random.randint(1, 9)
				
					# Vérification des diagonales pour 2 éléments côtes à côtes
				if diagonaleGD == [":one:", r":(o|x){1}:", r":(o|x){1}:"]:
					colonneBot = 0
					ligneBot = 0
				elif diagonaleGD == [r":(o|x){1}:", ":five:", r":(o|x){1}:"]:
					colonneBot = 1
					ligneBot = 1
				elif diagonaleGD == [r":(o|x){1}:", r":(o|x){1}:", ":nine:"]:
					colonneBot = 2
					ligneBot = 2
				elif diagonaleDG == [":three:", r":(o|x){1}:", r":(o|x){1}:"]:
					colonneBot = 2
					ligneBot = 0
				elif diagonaleDG == [r":(o|x){1}:", ":five:", r":(o|x){1}:"]:
					colonneBot = 1
					ligneBot = 1
				elif diagonaleDG == [r":(o|x){1}:", r":(o|x){1}:", ":seven:"]:
					colonneBot = 0
					ligneBot = 2
				else:
					if symboleBotPasDansGrilleListe == True:
						caseBot = random.randint(1, 9)
						if caseBot in casesInterdites19:
							while caseBot in casesInterdites19:
								caseBot = random.randint(1, 9)

				if caseBot == 1:
					colonneBot = 0
					ligneBot = 0
				elif caseBot == 2:
					colonneBot = 1
					ligneBot = 0
				elif caseBot == 3:
					colonneBot = 2
					ligneBot = 0
				elif caseBot == 4:
					colonneBot = 0
					ligneBot = 1
				elif caseBot == 5:
					colonneBot = 1
					ligneBot = 1
				elif caseBot == 6:
					colonneBot = 2
					ligneBot = 1
				elif caseBot == 7:
					colonneBot = 0
					ligneBot = 2
				elif caseBot == 8:
					colonneBot = 1
					ligneBot = 2
				elif caseBot == 9:
					colonneBot = 2
					ligneBot = 2

					# Le bot joue
				grilleListe[ligneBot][colonneBot] = symboleBot

					# Ajout des cases interdites quand le bot joue
				if ligneBot == 0 and colonneBot == 0:
					casesInterdites19.append(1)
					casesInterditesEmo.append(":one:")
				elif ligneBot == 0 and colonneBot == 1:
					casesInterdites19.append(2)
					casesInterditesEmo.append(":two:")
				elif ligneBot == 0 and colonneBot == 2:
					casesInterdites19.append(3)
					casesInterditesEmo.append(":three:")
				elif ligneBot == 1 and colonneBot == 0:
					casesInterdites19.append(4)
					casesInterditesEmo.append(":four:")
				elif ligneBot == 1 and colonneBot == 1:
					casesInterdites19.append(5)
					casesInterditesEmo.append(":five:")
				elif ligneBot == 1 and colonneBot == 2:
					casesInterdites19.append(6)
					casesInterditesEmo.append(":six:")
				elif ligneBot == 2 and colonneBot == 0:
					casesInterdites19.append(7)
					casesInterditesEmo.append(":seven:")
				elif ligneBot == 2 and colonneBot == 1:
					casesInterdites19.append(8)
					casesInterditesEmo.append(":eight:")
				elif ligneBot == 2 and colonneBot == 2:
					casesInterdites19.append(9)
					casesInterditesEmo.append(":nine:")



					# Si le bot a gagné, la partie est finie !
				if leBotAGagné == True:
					enPartieMorpion = False
					await client.edit_message(messageEnvoyeGrille, embed=discord.Embed(title="Morpion", description=messageGrille(grilleListe), footer="J'ai gagné :smiley:"))


##                               0       1       2
##                          0 -[0|0]- -[0|1]- -[0|2]-		[1] [2] [3]
##
##                          1  [1|0]   [1|1]   [1|2]		[4] [5] [6]
##
##                          2  [2|0]   [2|1]   [2|2]		[7] [8] [9]
##


				await client.edit_message(messageEnvoyeGrille, embed=discord.Embed(title="Morpion", description=messageGrille(grilleListe)))

		except Exception as ex:

			await client.send_message(message.channel, "```python\n" + str(ex) + "\n```")

	elif message.content.startswith(client.user.mention + " dit"):
		messageADireListe = message.content.split(" ")[2:]
		messageADire = ""
		for elements in messageADireListe:
			messageADire += elements + " "
		await client.send_message(message.channel, messageADire)

			# Report
	elif message.content.startswith(prefixe + "report") and message.author != client.user:
		report = message.content.split(" ")[1:]
		strReport = ""
		for elements in report:
		 	strReport += elements + " "
		strReport = strReport.capitalize()
		with open("reports.txt", "a") as reportsFile:
			reportsFile.write(strReport + "\n")
		await client.send_message(thedevkiller, strReport)


		#Si on mentionne le bot
	elif client.user.mentioned_in(message) and message.author != client.user:

		global demarreur
		demarreur = message.author

		global discussionChan
		discussionChan = message.channel

			# Ça va ?
		if re.match(".*(ça|sa|ca) va.? " + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".? (ça|sa|ca) va.*", message.content.lower()):
			await client.send_message(message.channel, "Ça va :smiley:, et toi ?")
			questioncava = True

			# Salut !
		elif re.match(".*(salut|slt|bonjour|salutations|hello|hi|hey|yo|coucou).? " + client.user.mention + ".*", message.content.lower()) != None or re.match(".*" + client.user.mention + ".? (salut|slt|bonjour|hello|hi|hey|yo).*", message.content.lower()) != None:
			await client.send_message(message.channel, "Salut " + message.author.mention + " !")

			# Quel est ton préfixe ?
		elif re.match(".*" + client.user.mention + ".? (quel|quelle|kel|c'est|c) (est|et) ton (prefixe|préfixe|prefix|préfixe) .*", message.content.lower()) or re.match(".*(quel|quelle|c'est) (est|et|koi|quoi) ton (prefixe|préfixe|prefix|préfix).? " + client.user.mention + ".*", message.content.lower()):
			await client.send_message(message.channel, "Mon préfixe est " + prefixe + ", n'hésite pas à dire " + prefixe + "help pour plus d'informations :wink:")

			# Tu fais quoi ?
		elif re.match(".*" + client.user.mention + ".? tu (fais|fait|fai) (quoi|koi).*", message.content) or re.match(".*tu (fais|fait|fai) (quoi|koi).? " + client.user.mention + ".*", message.content.lower()):
			await client.send_message(message.channel, "J'aide les gens, je joue et je discute avec eux :smiley:")

			# Insultes
		elif re.match(".*(tg|ta gueule|connard|connasse| con |taggle|fils de chien|enculé|batard|bâtard|pute|emmerde|stupide|salope|salaud|nique ta mère).{0,10}" + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,15}(tg|ta gueule|connard| con |fils de chien|enculé|batard|bâtard|pute|emmerde|stupide|salope|salaud|nique ta mère).*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,2} .{0,11} con$", message.content.lower()):
			await client.send_message(message.channel, "Pourquoi tu m'insulte ? :cry:")

			# C'est quoi ton code ?
		elif re.match(".*(c|c'est) (koi|quoi) ton (code|cod).*" + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".*(c|c'est) (koi|quoi) ton (code|cod).*", message.content.lower()):
			await client.send_message(message.channel, "https://github.com/TheDevKiller/TheBotKiller")

			# Je t'aime
		elif re.match(".*je (t'aime|taime).? " + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".? je (t'aime|taime)", message.content.lower()):
			await client.send_message(message.channel, "Moi aussi je t'aime " + message.author.mention + " :kissing_smiling_eyes:")

			# Crève
		elif re.match(".*(crève|meurt|meurts|crèves|buter).? " + client.user.mention + ".*", message.content.lower()):
			await client.send_message(message.channel, "Pourquoi tu dis ça ? :frowning:")

			# Je suis désolé
		elif re.match(".*(désolé|désolée|pardon|excuse).{0,15} " + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,2} désolé.*", message.content.lower()):
			await client.send_message(message.channel, "Bon allez je te pardonne :wink:")

			# Dis un message
		elif re.match('.*' + client.user.mention + '.? dis ".*', message.content.lower()):
			if re.match('.*dis ".*" à .* en privé.*', message.content.lower()):
				recherche = re.search('.*dis "(.*)" à (.*) ', message.content.lower())
				for elements in recherche:
					print(str(elements))

		elif message == client.user.mention or message == client.user.mention + " ?":
			await client.send_message("Oui ?")

			# Préfixe
		elif message.author == thedevkiller and str(message.content.split(" ")[1]) == "préfixe": # Changement du préfixe
			prefixe = str(message.content.split(" ")[2])
			await client.send_message(message.channel, "Mon préfixe est désormais" + " " + prefixe)
			print("Le préfixe de </TheBotKiller> est désormais " + prefixe)

		else: # J'ai pas compris
			await client.send_message(message.channel, "Tu peux répéter ? Je n'ai pas très bien compris :neutral_face:")

			# Insultes
	elif re.match(".*(taggle|ta geule|tg|conar|connar|conard|connard|connasse|conase|connase|conasse|bâtard|batard|batar| con |emmerde|pute|fils de chien|stupide|salope|salaud|nique ta mère|putain|merde|enculé).*", message.content.lower()) or re.match("^con .*", message.content.lower()) or re.match(".* con$", message.content.lower()) or re.match("^con$", message.content.lower()):
			await client.send_message(message.channel, "C'est pas bien de dire des gros mots :stuck_out_tongue_winking_eye: !")
			print("Y'a " + str(message.author.name) + " il a dit un gros mot. C'est pas bien")

			# Cheh !
	elif re.match(".*cheh.*", message.content.lower()) and message.author == thedevkiller:
		await client.send_message(message.channel, "Cheh !")

			# Ça va ?
	elif questioncava == True and message.author == demarreur and message.channel == discussionChan:
		if re.match(".*(non|mal|pas|^pas mal).*", message.content.lower()):
			await client.send_message(message.channel, "Ah mince :frowning:... On va te réconforter sur ce serveur :smiley:")
			questioncava = False

			# Oui
		elif re.match(".*(oui|tranquille|bien|super).*", message.content.lower()):
			await client.send_message(message.channel, "Parfait !")
			questioncava = False

		else: # Aucun des deux
			await client.send_message(message.chanel, "Ok")
			questioncava = False

client.run(token)


'''
1
2
3
4
5
6
7
8
9

":one:"
":two:"
":three:"
	":four:"
	":five:"
	":six:"
	":seven:"
	":eight:"
	":nine:"

'''