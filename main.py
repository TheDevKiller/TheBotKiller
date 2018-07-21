#!/usr/bin/python3
#coding: utf8

# Imports

import discord
import asyncio
import random
import re
import speedtest
import pickle
from functools import cmp_to_key
from urllib.request import urlopen, Request
import requests
import os

# /Imports

# Token

with open("token.txt", "r") as tokenFile:
	token = tokenFile.read()

# /Token

# TheCatApiKey

with open("catapikey.txt", "r") as catapikeyFile:
	catkey = catapikeyFile.read()

# Variables

commandes = \
"""
Si vous voulez, vous pouvez discuter avec moi :smiley:. Mentionnez-moi et si je ne suis pas trop occupé, je vous répondrais peut-être :wink:)

`report`: Je bug ? Je vous envoie une erreur ? Je triche ? Faites-le moi savoir grâce à cette commande avec l'erreur si il y en a une :wink:

`help`: Affiche cette page d'aide
`code`: Mon code sur Github
`shifumi <élément>`: Joue avec moi au shifumi !
`+- <min> <max>`: Joue avec moi au plus ou moins !
`speedtest`: Ma bonne connexion à la campagne :stuck_out_tongue:
`chat`: Des chats trop mignons :heart_eyes:
"""

# /Variables

# Fonctions

# def dlimg(url, filename):
# 	headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
# 	image = requests.Session().get(url, headers=headers).content
# 	with open(filename, "w+b") as fichierImage:
# 		fichierImage.write(image)


def chargerscorespom():
    global scoresPom
    scoresPom = {}
    try:
        with open("db/scoresPom.db", "rb") as fichierScoresPom:
            unpickler = pickle.Unpickler(fichierScoresPom)
            scoresPom = unpickler.load()
            print("Chargement: scoresPom chargé avec succès\n")
    except:
        scoresPom = {}
        print("Chargement: base de données scoresPom vide\n")
    return scoresPom

def sauverscorespom():
    global scoresPom
    with open("db/scoresPom.db", "wb") as fichierScoresPom:
        pickler = pickle.Pickler(fichierScoresPom)
        pickler.dump(scoresPom)

def ajouterscorespom(min, max, joueur, score):
    global scoresPom

    for elements in scoresPom:
    	scorePomSplit = scoresPom.split("-")
    	scoresPomATrier = scorePomSplit[0] + scoresPomSplit[2]
    	scoresPomTries = sorted(scoresPomATrier)

    print(scoresPomTries)

    if str(min) + "-" + str(max) not in scoresPom:
    	scoresPom[str(min) + "-" + str(max)] = {}
    	scoresPom[str(min) + "-" + str(max)][joueur] = score
    elif joueur not in scoresPom[str(min) + "-" + str(max)]:
    	scoresPom[str(min) + "-" + str(max)][joueur] = score     # TODO
    elif score < scoresPom[str(min) + "-" + str(max)][joueur]:   # Checker si la clé existe
    	scoresPom[str(min) + "-" + str(max)][joueur] = score

def print_scores():
    global scoresPom
    message = ""

    scoresPom = sorted(scoresPom, key=cmp_to_key(comparer))

    for minmax, scoreitems in scoresPom.items():
        message += "**" + minmax + "**\n"
        for player, score in scoreitems.items(): 
            message += str(player) + ": " + str(score) + " essais\n"
    return 

def comparer(arg1, arg2):
	if int(arg1.split("-")[0] + arg1.split("-")[1]) > int(arg2.split("-")[0] + arg2.split("-")[0]):
		return 1
	elif int(arg1.split("-")[0] + arg1.split("-")[1]) > int(arg2.split("-")[0] + arg2.split("-")[0]):
		return -1
	else:
		return 0


# /Fonctions

# Connexion

print("\nConnexion: Chargement de </TheBotKiller> ...")

client = discord.Client()

plusoumoins = False

@client.event
async def on_ready():
	global thedevkiller
	global scoresPom
	thedevkiller = await client.get_user_info("436105272310759426")
	print("Connexion: </TheBotKiller> est prêt à discuter avec les utilisateurs et à jouer avec eux !\n")
	await client.change_presence(game=discord.Game(name="&help (ou prefixe + help)"))
	chargerscorespom()

# /ConnexionCheh !

@client.event
async def on_message(message): # Dès qu'il y a un message

	global plusoumoins

	global questioncava

	global insulte
	
	global scoresPom

	try:
		insulte
	except:
		insulte = False

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
		print("Code: demandé par " + message.author.name + "\n")

		# Shifumi

	elif message.content.startswith(prefixe + "shifumi"): # Commence une partie de Shifumi

		print("Shifumi: partie commencée entre " + message.author.name + " et </TheBotKiller>")

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

		if resultat == "Égalité :neutral_face:":
			gagnant = "Aucun"
		elif resultat == "T'as gagné :frowning:":
			gagnant = message.author.name
		else:
			 gagnant = "</TheBotKiller>"

		jeuJoueur = jeuJoueur.split(" ")[0]
		elementBot = elementBot.split(" ")[0]

		print(message.author.name + " a joué " + jeuJoueur + " et </TheBotKiller> a joué " + elementBot + ". " + gagnant + " a gagné\n")

		# Help
	elif message.content.startswith(prefixe + "help"):
		await client.send_message(message.channel, embed=discord.Embed(title="Liste des commandes disponibles", description=commandes, color=0x0055FE))
		print("Aide: demandée par " + message.author.name + "\n")

		# Plus Ou Moins
	elif message.content.startswith(prefixe + "+- "):
		try:
			global joueurPom
			joueurPom = message.author
			global min
			global max
			min = int(message.content.split(" ")[1])
			max = int(message.content.split(" ")[2])
			if(min > max):
				min, max = max, min
			print("Plus ou moins: partie commencée par " + message.author.name + " avec un nombre entre " + str(min) + " et " + str(max))
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
	elif plusoumoins == True and message.author == joueurPom and message.channel == plusoumoinschan:
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
				print("Plus ou moins: " + message.author.name + " a trouvé le nombre en 1 essai. Le nombre était " + str(nombre) + "\n")
				ajouterscorespom(min, max, message.author.name, essais)
				sauverscorespom()
			else:
				await client.send_message(message.channel, "C'est ça, bien joué " + message.author.mention + " ! Tu as réussi en " + str(essais) + " essais")
				print("Plus ou moins: " + message.author.name + " a trouvé le nombre en " + str(essais) + " essais. Le nombre était " + str(nombre) + "\n")
				ajouterscorespom(min, max, message.author.name, essais)
				sauverscorespom()
			plusoumoins = False

			# Scores Plus Ou Moins
	elif message.content.startswith(prefixe + "+-scores"):
		await client.send_message(message.channel, embed=discord.Embed(title="Classement du Plus Ou Moins", description=print_scores(), color=0x17a81c))

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
			print("Dilemme: dans cette liste " + str(listeChoix) + ", </TheBotKiller> a choisi " + choix + "\n")

		except Exception as ex:
			await client.send_message(message.channel,"```\n" + str(ex) + "\n```")


			# Dire un message
	elif message.content.startswith(client.user.mention + " dis"):
		messageADireListe = message.content.split(" ")[2:]
		messageADire = ""
		for elements in messageADireListe:
			messageADire += elements + " "
		await client.send_message(message.channel, messageADire)
		print('Discussion: </TheBotKiller> a dit "' + messageADire + '"\n')

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
		print("Report: fait par " + message.author.name + ". Voir reports.txt.\n")

		# Speedtest
	elif message.content.startswith(prefixe + "speedtest"):
		messageChargement = await client.send_message(message.channel, "Recherche du meilleur serveur ...")
		test = speedtest.Speedtest()
		test.get_best_server()
		await client.edit_message(messageChargement, "Mesure du débit descendant")
		test.download()
		await client.edit_message(messageChargement, "Mesure du débit montant")
		test.upload()
		url = test.results.share()
		await client.delete_message(messageChargement)
		em = discord.Embed(title="** **Voilà ma bonne connexion de campagnard", color=0x012ea0)
		em.set_image(url=test.results.share())
		await client.send_message(message.channel, embed=em)
		print("Speedtest: fait par " + message.author.name + ". Les résultats sont " + test.results.share() + "\n")

		# Chat
	elif message.content.startswith(prefixe + "chat"):
		chaturl = "http://thecatapi.com/api/images/get?api_key=" + catkey
		req = Request(chaturl, headers={'User-Agent': "Bot"})
		resultchat = urlopen(req).geturl()
		em = discord.Embed(color=0xFF9100)
		em.set_image(url=resultchat)
		await client.send_message(message.channel, embed=em)
		print("Chat: " + message.author.name + " a demandé un chat\n")

		# Si on mentionne le bot
	elif client.user.mentioned_in(message) and message.author != client.user:

		print("Discussion:" + message.author.name + " discute avec </TheBotKiller>.\n")

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
		elif re.match(".*(tg|ta gueule|connard|connasse| con |taggle|fils de chien|enculé|batard|bâtard|pute|emmerde|salope|salaud|nique ta mère).{0,10}" + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,15}(tg|ta gueule|connard| con |fils de chien|enculé|batard|bâtard|pute|emmerde|stupide|salope|salaud|nique ta mère).*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,2} .{0,11} con$", message.content.lower()):
			await client.send_message(message.channel, "Pourquoi tu m'insulte ? :cry:")
			insulte = True

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
			print("Discussion: " + message.author.name + " a dit " + message.content + ". </TheBotKiller> n'a pas compris :/\n")

			# Insultes
	elif re.match(".*(taggle|ta geule|tg|conar|connar|conard|connard|connasse|conase|connase|conasse|bâtard|batard|batar| con |emmerde|pute|fils de chien|stupide|salope|salaud|nique ta mère|putain|merde|enculé).*", message.content.lower()) or re.match("^con .*", message.content.lower()) or re.match(".* con$", message.content.lower()) or re.match("^con$", message.content.lower()):
			await client.send_message(message.channel, "C'est pas bien de dire des gros mots :stuck_out_tongue_winking_eye: !")

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

	elif insulte == True and message.author != client.user:
		await client.send_message(message.channel, "C'est pas une raison ! :rage:")
		insulte = False

	elif re.match(".*je vais manger.*", message.content.lower()):
		await client.send_message(client.get_channel(401676021469937667), "Bon appétit " + message.author.mention)

async def on_member_join(member):
	await client.send_message(401668766683103233, )

# try:
# 	client.run(token)
# except:
# 	leBotEstCo = False
# 	while leBotEstCo == False:
# 		try:
# 			client.run(token)
# 			leBotEstCo = True
# 		except:
# 			pass
client.run(token)