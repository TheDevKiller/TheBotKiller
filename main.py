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

print("Chargement de </TheBotKiller> avec le token", token)

client = discord.Client()

global prefixe
prefixe = "&"

@client.event
async def on_ready():
	global thedevkiller
	thedevkiller = await client.get_user_info("436105272310759426")
	print("</TheBotKiller est prêt à discuter avec les utilisateurs et à jouer avec eux !")
	await client.change_presence(game=discord.Game(name="&help (ou prefixe + help)"))

@client.event
async def on_message(message): # Dès qu'il y a un message

	if client.user.mentioned_in(message) and message.author == thedevkiller: # Changement du préfixe
		global prefixe
		prefixe = message.content.split(" ")
		prefixe = str(prefixe[1])
		await client.send_message(message.channel, "Mon préfixe est désormais" + " " + prefixe)
		print("Le préfixe de </TheBotKiller> est désormais " + prefixe)

	elif message.content.startswith(prefixe + "code"): # Renvoie le lien Github
		await client.send_message(message.channel, "https://github.com/TheDevKiller/TheBotKiller")

	elif message.content.startswith(prefixe + "shifumi"): # Commence une partie de Shifumi
		elements = ["pierre", "feuille", "ciseaux"]
		jeuJoueur = message.content.split(" ")[1].lower()
		jeuBot = random.choice(elements)

		if jeuJoueur == jeuBot:                                 # La deuxième personne
			resultat = "Égalité"                            # du singulier signifie
		elif jeuJoueur == "pierre" and jeuBot == "feuille":     # le joueur
			resultat = "T'as perdu"
		elif jeuJoueur == "pierre" and jeuBot == "ciseaux":
			resultat = "T'as gagné"
		elif jeuJoueur == "feuille" and jeuBot == "pierre":
			resultat = "T'as gagné"
		elif jeuJoueur == "ciseaux" and jeuBot == "pierre":
			resultat = "T'as perdu"
		elif jeuJoueur == "feuille" and jeuBot == "ciseaux":
			resultat = "T'as perdu"
		elif jeuJoueur == "ciseaux" and jeuBot == "Feuille":
			resultat = "T'as gagné"
		else:
			await client.send_message(message.channel, "Entre un élément valide à la prochaine partie s'il te plaît :wink:")

		await client.send_message(message.channel, embed=discord.Embed(title="Résultat du Shifumi entre " + message.author.name + " et </TheBotKiller>", description="**Tu as joué: **\n" + jeuJoueur.capitalize() + "\n\n**J'ai joué: **\n" + jeuBot.capitalize() + "\n\n**Résultat: **\n" + resultat, color=0x00ff00))

	elif message.content.startswith(prefixe + "help"):
		await client.send_message(message.channel, embed=discord.Embed(title="Liste des commandes disponibles", description="`help`: Affiche cette page d'aide\n`code`: Mon code source (Github)\n`&shifumi <élément>`: Jouez avec moi à Shifumi !", color=0x0055FE))


client.run(token)