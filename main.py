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
async def on_ready:
	global thedevkiller
	thedevkiller = await client.get_user_infos("436105272310759426")
	print("</TheBotKiller est prêt à discuter avec les utilisateurs et à jouer avec eux !")


client.run(token)
