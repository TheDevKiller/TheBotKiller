#!/usr/bin/python3
# -*- coding: utf8 -*-

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
import nekos
from html import unescape
import json
from subprocess import call, run
import base64
import qrcode
import pytesseract
from PIL import Image
from pydub import AudioSegment
import sys
import traceback

##########
# Secret #
##########

with open("secrets.json", "r") as fichier:
	secrets = json.load(fichier)

#############
# Variables #
#############

	###########
	# Musique #
	###########

queue = []

voice = None

player = None

	########
	# Help #
	########

commandes = \
"""
Si vous voulez, vous pouvez discuter avec moi :smiley:. Mentionnez-moi et si je ne suis pas trop occupé, je vous répondrais peut-être :wink:)

:tools: **Utilitaires** :tools:

`report`: Reporter les bugs
`help`: Affiche cette page d'aide
`code`: Mon code sur Github
`speedtest`: Ma bonne connexion à la campagne :stuck_out_tongue:
`traduire <langue source> <langue cible> <texte>`: Traduction
`convertir <unité> <unité> <chaine>`: Converti la chaine de la première unité en la deuxième. Encode et decode aussi.
`qr <chaine>`: Génère un QR Code avec la chaine. Peut être
`ocr`: Poster une image avec la commande en commentaire. Vous donne son 
`tts <chaine>`: Dis votre texte grâce à la synthèse vocale :smiley:
`lower <chaine`: Passe le texte en minuscules
`upper <chaine`: Passe le texte en majuscules
`capitalize <chaine>`: Ajoute la majuscule à la première lettre et le reste en minuscules
`title <chaine>`: Ajoute une majuscule à chaque mot

:ping_pong: **Jeux** :ping_pong:

`shifumi <élément>`: Joue avec moi au shifumi !
`+- <min> <max>`: Joue avec moi au plus ou moins !

:upside_down: Fun :upside_down:

`dilemme <choix 1>, <choix 2>`: Si vous avez un dilemme ^^
`chat`: Des chats trop mignons :heart_eyes:
`ah`: Denis Brogniart
`obvious`: Merci captain obvious !
`non`: Mario qui dit non

:notes: **Musique** :notes:

`play <recherche>`: Me connecte à votre salon et joue de la musique
`stop`: Arrête la musique
`disconnect`: Me déconnecte des salons vocaux
"""

	###########
	# Clients #
	###########

client = discord.Client()

voiceclient = discord.VoiceClient

	##############
	# Discussion #
	##############

insulte = False

questioncava = False

	##########
	# Autres #
	##########

plusoumoins = False

flags = ['ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'ao', 'aq', 'ar', 'as', 'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bw', 'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'er', 'es', 'et', 'eu', 'fi', 'fj', 'fm', 'fo', 'fr', 'ga', 'gb', 'gd', 'ge', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gq', 'gr', 'gt', 'gu', 'gw', 'gy', 'hk', 'hn', 'hr', 'ht', 'hu', 'ic', 'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pn', 'pr', 'ps', 'pt', 'pw', 'py', 'qa', 'ro', 'rs', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'ss', 'st', 'sv']

headers = {"User-Agent": "Je suis un gentil bot qui vient en paix ^^"}

speedtestEnCours = False

prefixe = "&"

##############
# Paramètres #
##############

qr = qrcode.QRCode( # Paramètres du QR Code
	version=1,
	error_correction=qrcode.constants.ERROR_CORRECT_L,
	box_size=10,
	border=2
)

#############
# Fonctions #
#############

	###########
	# YouTube #
	###########

def getUrl(url) :
	req = Request(url, headers=headers)
	result = urlopen(req)
	result = unescape(result.read().decode("utf-8"))
	return json.loads(result)

	#################
	# Scores + OU - #
	#################

def chargerscorespom():
    global scoresPom
    scoresPom = {}
    try:
        with open("db/scoresPom.db", "rb") as fichierScoresPom:
            unpickler = pickle.Unpickler(fichierScoresPom)
            scoresPom = unpickler.load()
    except:
        scoresPom = {}
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

		##############
		# Traduction #
		##############

def translate(source, cible, chaine):
	url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + source + "&tl=" + cible + "&dt=t&q=" + chaine
	print(url)
	tradlist = requests.get(url, headers=headers).json()
	trad = tradlist[0][0][0]
	return trad



print("\nConnexion: Chargement de </TheBotKiller> ...")

##############
# Coroutines #
##############

@client.event
async def on_ready():
	global thedevkiller
	global scoresPom
	thedevkiller = await client.get_user_info("436105272310759426")
	print("Connexion: </TheBotKiller> est prêt à discuter avec les utilisateurs et à jouer avec eux !\n")
	await client.change_presence(game=discord.Game(name="&help (ou prefixe + help)"))
	try:
		if sys.argv[1] == "reboot": await client.send_message(sys.argv[2], "Je suis de retour, pour vous jouer un mauvais tour :smiling_imp:")
	except:
		pass
	chargerscorespom()

@client.event
async def on_error(event, *args, **kwargs):
 	print(event)
 	await client.send_message(message.channel, traceback.format_exc())

#############
# Commandes #
#############

@client.event
async def on_message(message):

	############
	# Globales #
	############

	global plusoumoins

	global questioncava

	global insulte
		
	global scoresPom

	global speedtestEnCours

	global player

	global voice

	global queue

	global prefixe

	#############
	# Anti-Bots #
	#############

	if message.author == client.user: return
	if "Bot" in [role.name for role in message.author.roles]: return

	############################
	# Extinction / Redémarrage #
	############################

		# Reboot
	if message.content.startswith(prefixe + "reboot"):
		if message.author == thedevkiller:
			print("Redémarrage ...")
			await client.send_message(message.channel, "Je reviens vite :wave:")
			await client.logout()
			run(["./reboot.sh", "401676021469937667"], shell=True)
			sys.exit(0)
		else:
			await client.send_message(message.channel, "Nope, je reste :smirk:")

		# Halt
	elif message.content.startswith(prefixe + "halt"):
		if message.author == thedevkiller:
			await client.send_message(message.channel, "Arrêt du bot ...")
			print("*Se couche* ...\n")
			client.logout()
			sys.exit(0)
			await client.send_message(message.channel, "Le bot est censé être arrêté donc si tu vois ce message, c'est pas normal")
		else:
			await client.send_message(message.channel, "Nan, j'ai pas trop envie de dormir là :neutral_face:")
	else:

		#############
		# Commandes #
		#############

			##############
			# Utilitaire #
			##############

			# Code
		if message.content.startswith(prefixe + "code"): # Envoie le lien Github
			await client.send_message(message.channel, "https://github.com/TheDevKiller/TheBotKiller")
			print("Code: demandé par " + message.author.name + "\n")

			# Help
		elif message.content.startswith(prefixe + "help"):
			await client.send_message(message.channel, embed=discord.Embed(title="Liste des commandes disponibles", description=commandes, color=0x0055FE))
			print("Aide: demandée par " + message.author.name + "\n")

			# Report
		elif message.content.startswith(prefixe + "report"):
			report = message.content.split(" ")[1:]
			strReport = ""
			for elements in report:
			 	strReport += elements + " "
			strReport += "\n" + message.author.name
			strReport = strReport.capitalize()
			with open("reports.txt", "a") as reportsFile:
				reportsFile.write(strReport + "\n")
			await client.send_message(thedevkiller, strReport)
			print("Report: fait par " + message.author.name + ". Voir reports.txt.\n")

			# Speedtest
		elif message.content.startswith(prefixe + "speedtest"):
			if speedtestEnCours == False:
				speedtestEnCours = True
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
				speedtestEnCours = False
			else:
				await client.send_message(message.channel, "Vous avez essayé de faire un speedtest, mais un autre était déjà en cours. Veuillez réessayer")
			
			# Translate
		elif message.content.startswith(prefixe + "traduire"):
			langue1 = message.content.split(" ")[1]
			langue2 = message.content.split(" ")[2]
			chaineListe = message.content.split(" ")[3:]
			chaine = ""
			for elements in chaineListe:
				chaine += elements + " "
			try:
				await client.send_message(message.channel, embed=discord.Embed(title="Traduction", description=langue1.capitalize() + ": " + chaine.capitalize() + "\n" + langue2.capitalize() + ": " + translate(langue1, langue2, chaine).capitalize(), colour=0xffffff))
				# if langue1 in flags and langue2 in flags:
				# 	em = discord.Embed(title="Traduction", description=":flag_" + langue1 + ":: " + chaine + "\n" + ":flag_" + langue2 + ":: " + translate(langue1, langue2, chaine))
				# 	await client.send_message(message.channel, embed=em)
				# else:
				# 	await client.send_message(message.channel, embed=discord.Embed(title="Traduction", ))
			except:
			 	await client.send_message(message.channel, "Spécifie une langue correcte avec ses deux premiers caractères (exemple: french => fr, english => en) s'il te plaît :wink:")

			# OCR
		elif message.content.startswith(prefixe + "ocr"):
			url = message.attachments[0]["url"]
			image = requests.Session().get(url).content
			fichier = message.attachments[0]["filename"]
			with open(fichier, "wb") as ocrimage:
				ocrimage.write(image)
			texte = pytesseract.image_to_string(Image.open(fichier))
			await client.send_message(message.channel, texte)
			os.remove(fichier)

			# TTS
		elif message.content.startswith(prefixe + "tts"):
			chaineliste = message.content.split(" ")[1:]
			chaine = ""
			for elements in chaineliste:
				chaine += elements + "%20"
			url = "http://api.voicerss.org/?key=c98f46f4fd494a07b3b64a021218b81c&hl=fr-fr&src=" + chaine
			audio = requests.Session().get(url, headers=headers).content
			with open("tts.mpga", "wb") as fichier:
				fichier.write(audio)
			#son = from_mpga("tts.mpga")
			#son.export("tts.mp3", format="mp3")
			await client.send_file(message.channel, "tts.mpga")

			# Flip
		elif message.content.startswith(prefixe + "flip"):
			dico = {"pile": "https://avocat-pau-lipsos.fr/wp-content/uploads/2016/08/250px-1_euro_pile.png",
			"face": "http://fracademic.com/pictures/frwiki/49/1_euro_France.png"}
			choix = random.choice(list(dico.keys()))
			em = discord.Embed(title=choix.capitalize() + " !")
			em.set_image(dico[choix])
			await client.send_message(message.channel, embed=em)

			########
			# Jeux #
			########

			# Shifumi
		elif message.content.startswith(prefixe + "shifumi"):

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

			#######
			# Fun #
			#######

			# Ah !
		elif message.content.startswith(prefixe + "ah"):
			await client.send_file(message.channel, "img/ah.jpg")
			print("Discussion: " + message.author.name + ": ah !")

			# Obvious
		elif message.content.startswith(prefixe + "obvious"):
			await client.send_file(message.channel, "img/obvious.jpg")
			print("Discussion: " + message.author.name + ": Merci captain obvious !")

			# Non
		elif message.content.startswith(prefixe + "non"):
			await client.send_file(message.channel, "img/non.jpg")
			print("Discussion: " + message.author.name + ": Non")



			# Joke
		elif message.content.startswith(prefixe + "joke"):
			await client.send_message(message.channel, requests.Session().get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"}).content.decode("utf-8"))
			print("Joke: " + message.author.name + " a demandé une blague")

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

			# Chat
		elif message.content.startswith(prefixe + "chat"):
			chaturl = nekos.cat()
			req = Request(chaturl, headers=headers)
			resultchat = urlopen(req).geturl()
			em = discord.Embed(color=0xFF9100)
			em.set_image(url=resultchat)
			await client.send_message(message.channel, embed=em)
			print("Chat: " + message.author.name + " a demandé un chat\n")

		###########
		# Musique #
		###########

			# Play
		elif message.content.startswith(prefixe + "play"):

			global lanceurmusique
			lanceurmusique = message.author

			recherchelist = message.content.split(" ")[1:]
			recherche = ""
			for index, elements in enumerate(recherchelist):
				if index != 0:
					recherche += "+" + elements
				else:
					recherche += elements
			jsonyt = getUrl("https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=" + recherche + "&key=" + secrets["youtube"])["items"][0]["id"]
			try:
				videoId = jsonyt["videoId"]
			except:
				await client.send_message(message.channel, "Le résultat trouvé n'est pas une vidéo.")
			url = "https://www.youtube.com/watch?v=" + videoId
			queue.append(url)
			try:
				voice = await client.join_voice_channel(message.author.voice.voice_channel)
			except:
				pass
			player = await voice.create_ytdl_player(url=url)
			player.start()
			print("\n")

			# Stop
		elif message.content.startswith(prefixe + "stop"): player.stop()
			
			# Disconnect
		elif message.content.startswith(prefixe + "disconnect"): await voice.disconnect()

			 	# Convertir
		elif message.content.startswith(prefixe + "convertir"):
			unite1 = message.content.split(" ")[1]
			unite2 = message.content.split(" ")[2]
			chaine = ""
			for elements in message.content.split(" ")[3:]:
				chaine += elements + " "
			if unite1 == "ascii" and unite2 == "base64":
				encode = base64.b64encode(str.encode(chaine))
				await client.send_message(message.channel, encode.decode())
			elif unite1 == "base64" and unite2 == "ascii":
				decode = base64.b64decode(str.encode(chaine))
				await client.send_message(message.channel, decode.decode().capitalize())
			elif unite1 == "ascii" and unite2 == "bin":
				encode = ' '.join(format(ord(x), 'b') for x in chaine)
				await client.send_message(message.channel, encode)
			elif unite1 == "bin" and unite2 == "ascii":
				chaine = int(chaine, 2)
				chaine.to_bytes((chaine.bit_length() + 7) // 8, "big").decode("utf-8", "surogatepass") or "\0"
				msg = ""
				for elements in chaine:
					for element in elements[::2]:
						msg += chr(element)
			else:
				await client.send_message(message.channel, "Désolé mais je ne connais pas ces unités :confused:")

				# QR Code
		elif message.content.startswith(prefixe + "qr"):
			chaineListe = message.content.split(" ")[1:]
			chaine = ""
			for elements in chaineListe:
				chaine += elements + " "
			qr.add_data(chaine)
			qr.make(fit=True)
			img = qr.make_image(fill_color="black", back_color="white")
			img.save("qr.png")
			await client.send_file(message.channel, "qr.png")
			await client.send_message(message.channel, chaine)
			os.remove("qr.png")

		######################
		# Formatage du texte #
		######################

			# Lower
		elif message.content.startswith(prefixe + "lower"):
			chaineliste = message.content.split(" ")[1:]
			chaine = ""
			for elements in chaineliste:
				chaine += elements + " "
			chaine = chaine.lower()
			print(chaine)
			await client.send_message(message.channel, chaine) 

			# Upper
		elif message.content.startswith(prefixe + "upper"):
			chaineliste = message.content.split(" ")[1:]
			chaine = ""
			for elements in chaineliste:
				chaine += elements + " "
			chaine = chaine.upper()
			print(chaine)
			await client.send_message(message.channel, chaine)

			# Capitalize
		elif message.content.startswith(prefixe + "capitalize"):
			chaineliste = message.content.split(" ")[1:]
			chaine = ""
			for elements in chaineliste:
				chaine += elements + " "
			chaine = chaine.capitalize()
			print(chaine)
			await client.send_message(message.channel, chaine)

			# Title
		elif message.content.startswith(prefixe + "title"):
			chaineliste = message.content.split(" ")[1:]
			chaine = ""
			for elements in chaineliste:
				chaine += elements + " "
			chaine = chaine.title()
			print(chaine)
			await client.send_message(message.channel, chaine)

			# Erreur
		elif message.content.startswith(prefixe + "erreur"):
			await client.send_message(erreur, xD)

			##############
			# Discussion #
			##############

			# Dire un message
		elif message.content.startswith(client.user.mention + " dis"):
			messageADireListe = message.content.split(" ")[2:]
			messageADire = ""
			for elements in messageADireListe:
				messageADire += elements + " "
			await client.send_message(message.channel, messageADire)
			print('Discussion: </TheBotKiller> a dit "' + messageADire + '"\n')

					# MRAW !!!
		elif re.match(".*mraw.*", message.content.lower()):
			await client.send_message(message.channel, "MRAW !!!")

			############
			# Mentions #
			############

			# Si on mentionne le bot
		elif client.user.mentioned_in(message):

			print("Discussion: " + message.author.name + " discute avec </TheBotKiller>.\n")

			global demarreur
			demarreur = message.author

			global discussionChan
			discussionChan = message.channel

				# Ça va ?
			if re.match(".*(ça|sa|ca) va.? " + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".? (ça|sa|ca) va.*", message.content.lower()):
				await client.send_message(message.channel, "Ça va :smiley:, et toi ?")
				questioncava = True
				print("Discussion: " + message.author.name + " a demandé à </TheBotKiller> si ça va\n")

				# Salut !
			elif re.match(".*(salut|slt|bonjour|salutations|hello|hi|hey|yo|coucou).? " + client.user.mention + ".*", message.content.lower()) != None or re.match(".*" + client.user.mention + ".? (salut|slt|bonjour|hello|hi|hey|yo).*", message.content.lower()) != None:
				await client.send_message(message.channel, "Salut " + message.author.mention + " !")
				print("Discussion: " + message.author.name + " a dis bonjour à </TheBotKiller>\n")

				# Quel est ton préfixe ?
			elif re.match(".*" + client.user.mention + ".? (quel|quelle|kel|c'est|c) (est|et) ton (prefixe|préfixe|prefix|préfixe) .*", message.content.lower()) or re.match(".*(quel|quelle|c'est) (est|et|koi|quoi) ton (prefixe|préfixe|prefix|préfix).? " + client.user.mention + ".*", message.content.lower()):
				await client.send_message(message.channel, "Mon préfixe est " + prefixe + ", n'hésite pas à dire " + prefixe + "help pour plus d'informations :wink:")
				print("Discussion: " + message.author.name + " a demandé le préfixe à </TheBotKiller>\n")

				# Tu fais quoi ?
			elif re.match(".*" + client.user.mention + ".? tu (fais|fait|fai) (quoi|koi).*", message.content) or re.match(".*tu (fais|fait|fai) (quoi|koi).? " + client.user.mention + ".*", message.content.lower()):
				await client.send_message(message.channel, "J'aide les gens, je joue et je discute avec eux :smiley:")
				print("Discussion: " + message.author.name + " a demandé à </TheBotKiller> ce qu'il fait\n")

				# Insultes
			elif re.match(".*(tg|ta gueule|connard|connasse| con |taggle|fils de chien|enculé|batard|bâtard|pute|emmerde|salope|salaud|nique ta mère).{0,10}" + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,15}(tg|ta gueule|connard| con |fils de chien|enculé|batard|bâtard|pute|emmerde|stupide|salope|salaud|nique ta mère).*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,2} .{0,11} con$", message.content.lower()):
				await client.send_message(message.channel, "Pourquoi tu m'insulte ? :cry:")
				insulte = True
				print("Discussion: " + message.author.name + " a insulté </TheBotKiller>")

				# C'est quoi ton code ?
			elif re.match(".*(c|c'est) (koi|quoi) ton (code|cod).*" + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".*(c|c'est) (koi|quoi) ton (code|cod).*", message.content.lower()):
				await client.send_message(message.channel, "https://github.com/TheDevKiller/TheBotKiller")
				print("Discussion: " + message.author.name + " a demandé à </TheBotKiller> son code")

				# Je t'aime
			elif re.match(".*je (t'aime|taime).? " + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".? je (t'aime|taime)", message.content.lower()):
				await client.send_message(message.channel, "Moi aussi je t'aime " + message.author.mention + " :kissing_smiling_eyes:")
				print("Discussion: " + message.author.name + " aime </TheBotKiller>")

				# Crève
			elif re.match(".*(crève|meurt|meurts|crèves|buter).? " + client.user.mention + ".*", message.content.lower()):
				await client.send_message(message.channel, "Pourquoi tu dis ça ? :frowning:")
				print("Discussion: " + message.author.name + " a dis à </TheBotKiller> de mourir :/")

				# Je suis désolé
			elif re.match(".*(désolé|désolée|pardon|excuse).{0,15} " + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,2} désolé.*", message.content.lower()):
				await client.send_message(message.channel, "Bon allez je te pardonne :wink:")
				print("Discussion: " + message.author.name + " s'est excusé auprès de </TheBotKiller>")

				# Oui ?
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

				# Cheh !
		elif re.match(".*cheh.*", message.content.lower()) and message.author == thedevkiller:
			await client.send_message(message.channel, "Cheh !")
			print("Discussion: " + message.author.name + " a dit cheh")

				# Ça va ?
		elif questioncava == True and message.author == demarreur and message.channel == discussionChan:
			if re.match(".*(non|mal|pas|^pas mal).*", message.content.lower()):
				await client.send_message(message.channel, "Ah mince :frowning:... On va te réconforter sur ce serveur :smiley:")
				questioncava = False
				print("Discussion: " + message.author.name + " a demandé à </TheBotKiller> si ça va ")

				# Oui
			elif re.match(".*(oui|tranquille|bien|super).*", message.content.lower()):
				await client.send_message(message.channel, "Parfait !")
				questioncava = False
				print("Discussion: " + message.author.name + " va bien")

			else: # Aucun des deux
				await client.send_message(message.chanel, "Ok")
				questioncava = False
				print("Discussion: " + message.author.name + " ne va pas bien")

			# C'est pas une raison !
		elif insulte == True:
			await client.send_message(message.channel, "C'est pas une raison ! :rage:")
			insulte = False
			print("Discussion: " + message.author.name + " </TheBotKiller> a dit que ce n'est pas uen raison !")

			# Bon appétit
		elif re.match(".*(je vais manger|je dois aller manger).*", message.content.lower()):
			await client.send_message(message.channel, "Bon appétit " + message.author.mention)
			print("Discussion: " + message.author.name + " va manger. </TheBotKiller> lui souhaite bon appétit")

		#########
		# Caché #
		#########

			# Neko
		elif message.content.startswith(prefixe + "neko"):
			arg = message.content.split(" ")[1]
			await client.send_message(message.channel, nekos.img((arg)))

client.run(secrets["discord"])