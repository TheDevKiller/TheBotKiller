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
import subprocess
import base64
import qrcode
import pytesseract
from PIL import Image
from pydub import AudioSegment
import sys
import traceback
import psutil

##########
# Secret #
##########

with open("secrets.json", "r") as fichier:
	secrets = json.load(fichier)

#############
# Variables #
#############

	########
	# Jeux #
	########

reactionsValides = ["🌑", "📄", "✂"]

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
`pc <arg>`: arg = infos/hardware donne des infos sur mon PC
`serveurs`: Donne la liste des serveurs où je suis
`membres`: La liste des membres sur le serveur

:regional_indicator_t: Formatage du texte :regional_indicator_t:

`lower <chaine>`: Passe le texte en minuscules
`upper <chaine>`: Passe le texte en majuscules
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
`canyrcmeyrb`: C'est à n'y rien comprendre, même en y réfléchissant bien !
`vdm`: Vie de merde :confused:

:notes: **Musique** :notes:

~~`play <recherche>`: Me connecte à votre salon et joue de la musique
`stop`: Arrête la musique
`disconnect`: Me déconnecte des salons vocaux~~
Indisponible suite au passage à discord.py rewrite. Veuillez patienter
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

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}

speedtestEnCours = False

prefixe = "&"

	########
	# Neko #
	########

agrumentsNeko = \
"""
feet: Pour les amateurs de pieds
yuri: Des bonnes lesbiennes
trap: Pour ceux qui aiment le changement de sexe x)
futanari: Pour ceux qui aiment le changement de sexe mais en gardant les bases :wink:
hololewd:
lewdkemo:
solog:
feetg:
cum:
erokemo:
les:
lewdk:
ngif:
tickle:
lewd: Pour ceux qui n'aiment pas la censure :smiley:
eroyuri:
eron:
cum_jpg:
bj:
nsfw_neko_gif:
solo:
kemonomimi:
nsfw_avatar:
poke:
anal:
slap:
hentai:
avatar:
erofeet:
holo:
keta:
blowjob:
pussy:
tits:
holoero:
lizard:
pussy_jpg:
pwankg:
classic:
kuni:
pat:
8ball:
kiss:
femdom:
neko:
cuddle:
erok:
fox_girl:
boobs:
random_hentai_gif:
smallboobs:
hug:
ero:
"""

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

	# Prêt
@client.event
async def on_ready():
	global thedevkiller
	global scoresPom
	thedevkiller = await client.get_user_info(436105272310759426)
	print("Connexion: </TheBotKiller> est prêt à discuter avec les utilisateurs et à jouer avec eux !\n")
	await client.change_presence(status=discord.Status.online, activity=discord.Game(name="&help (ou prefixe + help)"))
#	try:
#		if sys.argv[1] == "reboot": await client.send(sys.argv[2], "Je suis de retour, pour vous jouer un mauvais tour :smiling_imp:")
#	except:
#		pass
	chargerscorespom()

	# Erreurs
@client.event
async def on_error(event, *args, **kwargs):
	message = args[0]
	await message.channel.send(embed=discord.Embed(title="C'est con !", description="```python\n" + traceback.format_exc() + "\n```", color=0xff0000).set_footer(text="Ce message s'auto-déruira dans 1 min"), delete_after=60.0)
	await thedevkiller.send("```python\n" + traceback.format_exc() + "\n```")
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

	if message.author.bot: return

	############################
	# Extinction / Redémarrage #
	############################

		# Reboot
	if message.content.startswith(prefixe + "reboot"):
		if message.author == thedevkiller:
			print("Redémarrage ...")
			await message.channel.send("Je reviens vite :wave:")
			await client.logout()
			subprocess.run(["./reboot.sh", "401676021469937667"], shell=True)
			sys.exit(0)
		else:
			await message.channel.send("Nope, je reste :smirk:")
			print(message.author.name + " a voulu redémarré </TheBotKiller>. Vilain !")

		# Halt
	elif message.content.startswith(prefixe + "halt"):
		if message.author == thedevkiller:
			await message.channel.send("Je dois y aller, salut :wave:")
			print("*Se couche* ...\n")
			client.logout()
			sys.exit(0)
		else:
			await message.channel.send("Nan, j'ai pas trop envie de dormir là :neutral_face:")
	else:

		#############
		# Commandes #
		#############

			##############
			# Utilitaire #
			##############

			# Test
		if message.content.startswith(prefixe + "test"):
			await message.channel.send("Ce message s'autodétruira dans 5 secondes", delete_after=5.0)

			# PC
		elif message.content.startswith(prefixe + "pc"):
			if message.content.strip() == "&pc":
				await message.channel.send("Voulez-vous en savoir plus sur le `hardware` ou les `infos` ?")
			elif message.content.split(" ")[1] == "infos":

					# Load Average
				la = ""
				for index, elements in enumerate(os.getloadavg()):
					if index != 2: la += "**" + str(elements) + "**" + " | " 
					elif index == 2: la += "**" + str(elements) + "**"

					# Uptime
				uptimeplst = subprocess.check_output(["uptime", "-p"]).decode().split(" ")[1:]
				uptimep = ""
				for elements in uptimeplst:
					uptimep += elements + " "

				st = os.statvfs("/")
				used = round((st.f_blocks - st.f_bfree) * st.f_frsize / 1000000000, 1)
				total = round(st.f_blocks * st.f_frsize / 1000000000, 1)

					# Color
				if float(la.split(" ")[0].replace("**", "")) <= 3: color = 0x00ff00
				elif float(la.split(" ")[0].replace("**", "")) > 3 and float(la.split(" ")[0].replace("**", "")) < 4: color = 0xFF6D00
				elif float(la.split(" ")[0].replace("**", "")) >= 4: color = 0xff000
				else: color = 0xffffff

					# Batterie
				btoutput = subprocess.check_output(["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT1"])
				batterie = re.search("percentage:          (.{2})", btoutput.decode())[1]

				em = discord.Embed(title="<:server:452826125584826378> Mon PC - Infos", color=color)
				em.add_field(name="<:level_slider:474325122904489984> Load Average", value=la) # Load Average
				em.add_field(name="<:cpu:452823427137667089> CPU", value="**" + str(psutil.cpu_percent()) + "%**") # CPU Percent
				em.add_field(name="<:computerram:452824190475698187> RAM", value="**" + str(psutil.virtual_memory().percent) + "% **") # RAM Percent
				#uptimeEmoteNbre = subprocess.check_output("uptime").split(" ")[3]
				em.add_field(name=":clock10: Uptime", value="**" + uptimep.replace("week", "semaine").replace("day","jour").replace("hour","heure") + "**") # Uptime
				em.add_field(name="<:ubuntu:465194164548665345> OS", value="**Ubuntu 18.04 LTS**") # OS
				em.add_field(name="💾 Espace utilisé", value="**" + str(used) + "**" + "/" + "**" + str(total) + "** GB")
				em.add_field(name=":battery: Batterie", value="**" + batterie + "**%")
				await message.channel.send(embed=em)

				# Hardware
			elif message.content.split(" ")[1] == "hardware":
				em = discord.Embed(title="<:server:452826125584826378> Mon PC - Hardware", color=0x106b02)
				em.add_field(name=":computer: Modèle", value="**MSI CX62 6QD 249XFR**")
				em.add_field(name="<:nvidia:474722211391995904> Carte graphique", value="**NVIDIA 940MX 2**GB")
				em.add_field(name="<:intel:474722665752428569> Processeur", value="**Intel core i3 2 coeurs**")
				em.add_field(name="<:computerram:452824190475698187> RAM", value="**4GB DDR4**")
				em.add_field(name=":desktop: Écran", value="**Mat 1366**x**768** **15**.**6**\" **16**:**9**")
				em.add_field(name=":battery: Batterie", value="**Lithium**-**ion**")
				em.add_field(name="💾 Disque Dur", value="**HDD 500**GB")

				await message.channel.send(embed=em)
			else:
				await message.channel.send("Voulez-vous en savoir plus sur le `hardware` ou les `infos` ?")

			# Serveurs
		elif message.content.startswith(prefixe + "serveurs"):
			serveurs = "** **\n"
			servnbre = 0
			for elements in client.guilds:
				serveurs += "- " + elements.name + "\n\n" 
				servnbre += 1
			em = discord.Embed(title="<:server:452826125584826378> Serveurs", description=serveurs + "Je suis actuellement sur **" + str(servnbre) + "** serveurs", color=0x0294fc)
			await message.channel.send(embed=em)

			# Membres
		elif message.content.startswith(prefixe + "membres"):

			status = \
			{"online": {"False": 0, "True": 0},
			"offline": {"False": 0, "True": 0},
			"idle": {"False": 0, "True": 0},
			"dnd": {"False": 0, "True": 0}}

			for membre in message.guild.members:
				status[str(membre.status)][str(membre.bot)] += 1

			em = discord.Embed(title=":busts_in_silhouette: Membres", description="Total: **{}**".format(status["online"]["False"] + status["offline"]["False"] + status["idle"]["False"] + status["dnd"]["False"] + status["online"]["True"] + status["offline"]["True"] + status["idle"]["True"] + status["dnd"]["True"]), color=0x6817ff)
			em.add_field(name=":robot: Bots", value="Total: **{total}**\nEn ligne: **{online}**\nNe pas déranger: **{dnd}**\nAbsent: **{idle}**\nHors ligne: **{offline}**".format(total=status["online"]["True"] + status["offline"]["True"] + status["idle"]["True"] + status["dnd"]["True"], online=status["online"]["True"], offline=status["offline"]["True"], idle=status["idle"]["True"], dnd=status["dnd"]["True"]))
			em.add_field(name=":raising_hand: Humains", value="Total: **{total}**\nEn ligne: **{online}**\nNe pas déranger: **{dnd}**\nAbsent: **{idle}**\nHors ligne: **{offline}**".format(total=status["online"]["False"] + status["offline"]["False"] + status["idle"]["False"] + status["dnd"]["False"], online=status["online"]["False"], offline=status["offline"]["False"], idle=status["idle"]["False"], dnd=status["dnd"]["False"]))


			await message.channel.send(embed=em)

			# Shell
#		elif message.content.startswith(prefixe + "shell"):
#			if message.author == thedevkiller:
#				commandeliste = message.content.split(" ")[1:]
#				commande = " "
#				for elements in commandeliste:
#					commande += elements + " "
#				proc = subprocess.Popen(commandeliste, stdout=subprocess.PIPE)
#				output = proc.stdout.read().decode()
#				while len(output)>2000:
#					await message.channel.send(output[0:1999])
#					output = output[1990:]	
#			else:
#				await message.channel.send("Tu veux faire n'importe quoi sur mon PC ! Nan mais tu t'es cru où là ?!")		

			# Code
		elif message.content.startswith(prefixe + "code"): # Envoie le lien Github
			await message.channel.send("https://github.com/TheDevKiller/TheBotKiller")
			print("Code: demandé par " + message.author.name + "\n")

			# Help
		elif message.content.startswith(prefixe + "help"):
			await message.channel.send(embed=discord.Embed(title="Liste des commandes disponibles", description=commandes, color=0x0055FE))
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
			await thedevkiller.send(strReport)
			print("Report: fait par " + message.author.name + ". Voir reports.txt.\n")

			# Speedtest
		elif message.content.startswith(prefixe + "speedtest"):
			if speedtestEnCours == False:
				speedtestEnCours = True
				messageChargement = await message.channel.send("Recherche du meilleur serveur ...")
				test = speedtest.Speedtest()
				test.get_best_server()
				await messageChargement.edit(content = "Mesure du débit descendant")
				test.download()
				await messageChargement.edit(content = "Mesure du débit montant")
				test.upload()
				url = test.results.share()
				await messageChargement.delete()
				em = discord.Embed(title="** **Voilà ma bonne connexion de campagnard", color=0x012ea0)
				em.set_image(url=test.results.share())
				await message.channel.send(embed=em)
				print("Speedtest: fait par " + message.author.name + ". Les résultats sont " + test.results.share() + "\n")
				speedtestEnCours = False
			else:
				await message.channel.send("Vous avez essayé de faire un speedtest, mais un autre était déjà en cours. Veuillez réessayer")
			
			# Translate
		elif message.content.startswith(prefixe + "traduire"):
			langue1 = message.content.split(" ")[1]
			langue2 = message.content.split(" ")[2]
			chaineListe = message.content.split(" ")[3:]
			chaine = ""
			for elements in chaineListe:
				chaine += elements + " "
			try:
				await message.channel.send(embed=discord.Embed(title="Traduction", description=langue1.capitalize() + ": " + chaine.capitalize() + "\n" + langue2.capitalize() + ": " + translate(langue1, langue2, chaine).capitalize(), colour=0xffffff))
				# if langue1 in flags and langue2 in flags:
				# 	em = discord.Embed(title="Traduction", description=":flag_" + langue1 + ":: " + chaine + "\n" + ":flag_" + langue2 + ":: " + translate(langue1, langue2, chaine))
				# 	await client.send(message.channel, embed=em)
				# else:
				# 	await client.send(message.channel, embed=discord.Embed(title="Traduction", ))
			except:
			 	await message.channel.send("Spécifie une langue correcte avec ses deux premiers caractères (exemple: french => fr, english => en) s'il te plaît :wink:")

			# OCR
		elif message.content.startswith(prefixe + "ocr"):
			print(message.attachments)
			url = message.attachments[0]["url"]
			image = requests.Session().get(url).content
			fichier = message.attachments[0]["filename"]
			with open(fichier, "wb") as ocrimage:
				ocrimage.write(image)
			texte = pytesseract.image_to_string(Image.open(fichier))
			await message.channel.send(texte)
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
			with open("tts.mpa") as fichier:
				await message.channel.send(file=discord.File(fichier))

			# Flip
		elif message.content.startswith(prefixe + "flip"):
			dico = {"pile": "https://avocat-pau-lipsos.fr/wp-content/uploads/2016/08/250px-1_euro_pile.png",
			"face": "http://fracademic.com/pictures/frwiki/49/1_euro_France.png"}
			choix = random.choice(list(dico.keys()))
			em = discord.Embed(title=choix.capitalize() + " !")
			em.set_image(url=dico[choix])
			await message.channel.send(embed=em)
			print("Flip: " + message.author.name + " a lancé une pièce. Elle est retombée sur " + choix)

			########
			# Jeux #
			########

			# Shifumi
		elif message.content.startswith(prefixe + "shifumi"):

			print("Shifumi: partie commencée entre " + message.author.name + " et </TheBotKiller>")

			messageJoue = await message.channel.send(embed=discord.Embed(title="Shifumi", description="Joue :wink:", color=0xff7400))

			await messageJoue.add_reaction("🌑")
			await messageJoue.add_reaction("📄")
			await messageJoue.add_reaction("✂")

			reaction = await client.wait_for("reaction_add", check=lambda r, u: u.id == message.author.id)

			print(reaction[1].id)

			while reaction[0].emoji not in reactionsValides:
				await message.channel.send("Réagis avec pierre, feuille ou ciseaux :wink:")
				reaction = await client.wait_for("reaction_add", check=lambda r, u: u.id == message.author.id)

			while reaction[1].id != message.author.id:
				await message.channel.send("C'est là je vais mettre le nom du joueur logiquement qui a lancé la partie, pas toi ! :stuck_out_tongue_winking_eye:")
				reaction = await client.wait_for("reaction_add", check=lambda r, u: u.id == message.author.id)

			if reaction[0].emoji == "🌑":
				jeuJoueur = "pierre :new_moon:"
			elif reaction[0].emoji == "📄":
				jeuJoueur = "feuille :page_facing_up:"
			elif reaction[0].emoji == "✂":
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

			await messageJoue.edit(embed=discord.Embed(title="Résultat du Shifumi entre " + message.author.name + " et </TheBotKiller>", description="** **\n**Tu as joué: **\n\n" + jeuJoueur.capitalize() + "\n\n**J'ai joué: **\n\n" + elementBot.capitalize() + "\n\n**Résultat: **\n\n" + resultat, color=0xff7400))

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
			global joueurPom
			joueurPom = message.author
			global min
			global max
			min = int(message.content.split(" ")[1])
			max = int(message.content.split(" ")[2])
			if(min > max):
				min, max = max, min
			print("Plus ou moins: partie commencée par " + message.author.name + " avec un nombre entre " + str(min) + " et " + str(max))
			await message.channel.send("Devine à quel nombre je pense entre " + str(min) + " et " + str(max))
			global nombre
			nombre = random.randint(min, max)
			global plusoumoinschan 
			plusoumoinschan = message.channel
			plusoumoins = True
			global essais
			essais = 1

			# Plus Ou Moins
		elif plusoumoins == True and message.author == joueurPom and message.channel == plusoumoinschan:
			nombreJoueur = int(message.content)
			if nombreJoueur < nombre:
				await message.channel.send("C'est plus !")
				essais += 1
			elif nombreJoueur > nombre:
				await message.channel.send("C'est moins !")
				essais += 1
			elif nombreJoueur == nombre:
				if essais <= 1:
					await message.channel.send("C'est ça, bien joué {mention} ! Tu as réussi en {essais} essais".format(aut=message.author.mention, essais=essais))
					print("Plus ou moins: {aut} a trouvé le nombre en 1 essai. Le nombre était {nbre}\n".format(aut=message.author.name, nbre=nombre))
					ajouterscorespom(min, max, message.author.name, essais)
					sauverscorespom()
				else:
					await message.channel.send("C'est ça, bien joué {mention} ! Tu as réussi en {essais} essais".format(aut=message.author.mention, essais=essais))
					print("Plus ou moins: {aut} a trouvé le nombre en {essais} essais. Le nombre était {nbre}\n".format(aut=message.author.name, essais=essais, nbre=nombre))
					ajouterscorespom(min, max, message.author.name, essais)
					sauverscorespom()
				plusoumoins = False

			# Scores Plus Ou Moins
		elif message.content.startswith(prefixe + "+-scores"):
			await message.channel.send(embed=discord.Embed(title="Classement du Plus Ou Moins", description=print_scores(), color=0x17a81c))

			#######
			# Fun #
			#######

			# Ah !
		elif message.content.startswith(prefixe + "ah"):
			file_path = "img/ah.jpg"
			with open(file_path, "rb") as file:
				await message.channel.send(file=discord.File(file))
			print("Discussion: {aut}: ah !".format(aut=message.author.name))

			# Obvious
		elif message.content.startswith(prefixe + "obvious"):
			file_path = "img/obvious.jpg"
			with open(file_path, "rb") as file:
				await message.channel.send(file=discord.File(file))
			print("Discussion: {aut}: Merci captain obvious !".format(aut=message.author.name))

			# Non
		elif message.content.startswith(prefixe + "non"):
			file_path = "img/non.jpg"
			with open(file_path, "rb") as file:
				await message.channel.send(file=discord.File(file))
			print("Discussion: {aut}: Non".format(aut=message.author.name))

			# VDM
		elif message.content.startswith(prefixe + "vdm"):
			source = requests.Session().get("https://www.viedemerde.fr/aleatoire", headers=headers).content
			vdm = re.search(r"<p class=\"block hidden-xs\">\n<a href=\".*\">\n(.*) VDM", source.decode())[1]
			await message.channel.send(vdm)

			# C'est à n'y rien comprendre
		#elif message.content.startswith(prefixe + "canyrcmeyrb"):

			# DansTonChat
		elif message.content.startswith(prefixe + "dtc"):
			source = requests.Session().get("https://danstonchat.com/random0.html", headers={'Cache-Control': 'no-cache'}).content.decode()
			chat = re.search(r"<div class=\"addthis_inline_share_toolbox\" data-url=\"http:\/\/danstonchat\.com\/.{4}\" data-title=\"Dans Ton Chat n°.{4}\" data-description=\"(.+?)\" data-media=\"https://danstonchat\.com/icache/size/.{3}c.{3}/themes/danstonchat.{4}/images/logo-og\.png\">", source, flags=re.S)
			await message.channel.send(chat)

			# Joke
		elif message.content.startswith(prefixe + "joke"):
			await message.channel.send(requests.Session().get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"}).content.decode("utf-8"))
			print("Joke: {aut} a demandé une blague".format(aut=message.author.name))

			# Dilemme
		elif message.content.startswith(prefixe + "dilemme"):
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
			await message.channel.send("Je dirais " + choix.lower())
			print("Dilemme: dans cette liste {lst}, </TheBotKiller> a choisi {choix}\n".format(lst=listeChoix, choix=choix))

			# Chat
		elif message.content.startswith(prefixe + "chat"):
			chaturl = nekos.cat()
			req = Request(chaturl, headers=headers)
			resultchat = urlopen(req).geturl()
			em = discord.Embed(color=0xFF9100)
			em.set_image(url=resultchat)
			await message.channel.send(embed=em)
			print("Chat: {} a demandé un chat\n".format(message.author.name))

			# Convertir
		elif message.content.startswith(prefixe + "convertir"):
			unite1 = message.content.split(" ")[1]
			unite2 = message.content.split(" ")[2]
			chaine = ""
			for elements in message.content.split(" ")[3:]:
				chaine += elements + " "
			if unite1 == "ascii" and unite2 == "base64":
				encode = base64.b64encode(str.encode(chaine))
				await message.channel.send(encode.decode())
			elif unite1 == "base64" and unite2 == "ascii":
				decode = base64.b64decode(str.encode(chaine))
				await message.channel.send(decode.decode().capitalize())
			elif unite1 == "ascii" and unite2 == "bin":
				encode = ' '.join(format(ord(x), 'b') for x in chaine)
				await message.channel.send(encode)
			elif unite1 == "bin" and unite2 == "ascii":
				chaine = int(chaine, 2)
				chaine.to_bytes((chaine.bit_length() + 7) // 8, "big").decode("utf-8", "surogatepass") or "\0"
				msg = ""
				for elements in chaine:
					for element in elements[::2]:
						msg += chr(element)
			else:
				await message.channel.send("Désolé mais je ne connais pas ces unités :confused:")

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
			with open("qr.png", "rb") as qrimg:
				await message.channel.send(file=discord.File(qrimg))
			await message.channel.send(chaine)
			os.remove("qr.png")

			# Fortune
		elif message.content.startswith(prefixe + "fortune"):
			await message.channel.send("```\n{}\n```".format(subprocess.check_output("fortune").decode()))


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
			await message.channel.send(chaine) 

			# Upper
		elif message.content.startswith(prefixe + "upper"):
			chaineliste = message.content.split(" ")[1:]
			chaine = ""
			for elements in chaineliste:
				chaine += elements + " "
			chaine = chaine.upper()
			print(chaine)
			await message.channel.send(chaine)

			# Capitalize
		elif message.content.startswith(prefixe + "capitalize"):
			chaineliste = message.content.split(" ")[1:]
			chaine = ""
			for elements in chaineliste:
				chaine += elements + " "
			chaine = chaine.capitalize()
			print(chaine)
			await message.channel.send(chaine)

			# Title
		elif message.content.startswith(prefixe + "title"):
			chaineliste = message.content.split(" ")[1:]
			chaine = ""
			for elements in chaineliste:
				chaine += elements + " "
			chaine = chaine.title()
			print(chaine)
			await message.channel.send(chaine)

			# Erreur
		elif message.content.startswith(prefixe + "erreur"):
			raise NameError("Eh bah tu l'as ton erreur ! !")	
		
			##############
			# Discussion #
			##############

			# Dire un message
		elif message.content.startswith(client.user.mention + " dis") or message.content.startswith(prefixe + "dis"):
			messageADireListe = message.content.split(" ")[2:]
			messageADire = ""
			for elements in messageADireListe:
				messageADire += elements + " "
			await message.channel.send(messageADire)
			print('Discussion: </TheBotKiller> a dit "{msg}" suite à la demande de {aut} \n'.format(msg=message.content, aut=message.author.name))

					# MRAW !!!
		elif re.match(".*mraw.*", message.content.lower()):
			await message.channel.send("MRAW !!!")

			############
			# Mentions #
			############

			# Si on mentionne le bot
		elif client.user.mentioned_in(message):

			print("Discussion: {} discute avec </TheBotKiller>.\n".format(message.author.name))

			global demarreur
			demarreur = message.author

			global discussionChan
			discussionChan = message.channel

				# Ça va ?
			if re.match(".*(ça|sa|ca) va.? " + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".? (ça|sa|ca) va.*", message.content.lower()):
				await message.channel.send("Ça va :smiley:, et toi ?")
				questioncava = True
				print("Discussion: " + message.author.name + " a demandé à </TheBotKiller> si ça va\n")

				# Salut !
			elif re.match(".*(salut|slt|bonjour|salutations|hello|hi|hey|yo|coucou).? " + client.user.mention + ".*", message.content.lower()) != None or re.match(".*" + client.user.mention + ".? (salut|slt|bonjour|hello|hi|hey|yo).*", message.content.lower()) != None:
				await message.channel.send("Salut " + message.author.mention + " !")
				print("Discussion: " + message.author.name + " a dis bonjour à </TheBotKiller>\n")

				# Quel est ton préfixe ?
			elif re.match(".*" + client.user.mention + ".? (quel|quelle|kel|c'est|c) (est|et) ton (prefixe|préfixe|prefix|préfixe) .*", message.content.lower()) or re.match(".*(quel|quelle|c'est) (est|et|koi|quoi) ton (prefixe|préfixe|prefix|préfix).? " + client.user.mention + ".*", message.content.lower()):
				await message.channel.send("Mon préfixe est " + prefixe + ", n'hésite pas à dire " + prefixe + "help pour plus d'informations :wink:")
				print("Discussion: " + message.author.name + " a demandé le préfixe à </TheBotKiller>\n")

				# Tu fais quoi ?
			elif re.match(".*" + client.user.mention + ".? tu (fais|fait|fai) (quoi|koi).*", message.content) or re.match(".*tu (fais|fait|fai) (quoi|koi).? " + client.user.mention + ".*", message.content.lower()):
				await message.channel.send("J'aide les gens, je joue et je discute avec eux :smiley:")
				print("Discussion: " + message.author.name + " a demandé à </TheBotKiller> ce qu'il fait\n")

				# Insultes
			elif re.match(".*(tg|ta gueule|connard|connasse| con |taggle|fils de chien|enculé|batard|bâtard|pute|emmerde|salope|salaud|nique ta mère).{0,10}" + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,15}(tg|ta gueule|connard| con |fils de chien|enculé|batard|bâtard|pute|emmerde|stupide|salope|salaud|nique ta mère).*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,2} .{0,11} con$", message.content.lower()):
				await message.channel.send("Pourquoi tu m'insulte ? :cry:")
				insulte = True
				print("Discussion: " + message.author.name + " a insulté </TheBotKiller>")

				# C'est quoi ton code ?
			elif re.match(".*(c|c'est) (koi|quoi) ton (code|cod).*" + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".*(c|c'est) (koi|quoi) ton (code|cod).*", message.content.lower()):
				await message.channel.send("https://github.com/TheDevKiller/TheBotKiller")
				print("Discussion: " + message.author.name + " a demandé à </TheBotKiller> son code")

				# Je t'aime
			elif re.match(".*je (t'aime|taime).? " + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".? je (t'aime|taime)", message.content.lower()):
				await message.channel.send("Moi aussi je t'aime " + message.author.mention + " :kissing_smiling_eyes:")
				print("Discussion: " + message.author.name + " aime </TheBotKiller>")

				# Crève
			elif re.match(".*(crève|meurt|meurts|crèves|buter).? " + client.user.mention + ".*", message.content.lower()):
				await message.channel.send("Pourquoi tu dis ça ? :frowning:")
				print("Discussion: " + message.author.name + " a dis à </TheBotKiller> de mourir :/")

				# Je suis désolé
			elif re.match(".*(désolé|désolée|pardon|excuse).{0,15} " + client.user.mention + ".*", message.content.lower()) or re.match(".*" + client.user.mention + ".{0,2} désolé.*", message.content.lower()):
				await message.channel.send("Bon allez je te pardonne :wink:")
				print("Discussion: " + message.author.name + " s'est excusé auprès de </TheBotKiller>")

				# Oui ?
			elif message == client.user.mention or message == client.user.mention + " ?":
				await message.channel.send("Oui ?")

				# Préfixe
			elif message.author == thedevkiller and str(message.content.split(" ")[1]) == "préfixe": # Changement du préfixe
				prefixe = str(message.content.split(" ")[2])
				await message.channel.send("Mon préfixe est désormais" + " " + prefixe)
				print("Le préfixe de </TheBotKiller> est désormais " + prefixe)

				# Cheh !
		elif re.match(".*cheh.*", message.content.lower()) and message.author == thedevkiller:
			await message.channel.send("Cheh !")
			print("Discussion: " + message.author.name + " a dit cheh")

				# Ça va ?
		elif questioncava == True and message.author == demarreur and message.channel == discussionChan:
			if re.match(".*(non|mal|pas|^pas mal).*", message.content.lower()):
				await message.channel.send("Ah mince :frowning:... On va te réconforter sur ce serveur :smiley:")
				questioncava = False
				print("Discussion: " + message.author.name + " a demandé à </TheBotKiller> si ça va ")

				# Oui
			elif re.match(".*(oui|tranquille|bien|super).*", message.content.lower()):
				await message.channel.send("Parfait !")
				questioncava = False
				print("Discussion: " + message.author.name + " va bien")

			else: # Aucun des deux
				await message.channel.send("Ok")
				questioncava = False
				print("Discussion: " + message.author.name + " ne va pas bien")

			# C'est pas une raison !
		elif insulte == True:
			await message.channel.send("C'est pas une raison ! :rage:")
			insulte = False
			print("Discussion: " + message.author.name + " </TheBotKiller> a dit que ce n'est pas uen raison !")

			# Bon appétit
		elif re.match(".*(je vais manger|je dois aller manger).*", message.content.lower()):
			await message.channel.send("Bon appétit " + message.author.mention)
			print("Discussion: " + message.author.name + " va manger. </TheBotKiller> lui souhaite bon appétit")

		#########
		# Caché #
		#########

			# Neko
		elif message.content.startswith(prefixe + "neko"):
			if message.channel.is_nsfw():
				arg = message.content.split(" ")[1]
				try:
					await message.channel.send(nekos.img((arg)))
				except nekos.errors.InvalidArgument:
					await message.channel.send("Entre un argument valide :wink:\n Arguments: ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les', 'lewdk', 'ngif', 'meow', 'tickle', 'lewd', 'feed', 'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg', 'pwankg', 'classic', 'kuni', 'pat', '8ball', 'kiss', 'femdom', 'neko', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif', 'smallboobs', 'hug', 'ero']")
			else:
				await message.channel.send("Tu va choquer des gens :scream: ! Vas dans un salon NSFW enfin !")

client.run(secrets["discord"])
