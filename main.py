#!/usr/bin/python3
#-*- coding: utf8 -*-

###########
# Imports #
###########

import discord
from discord.ext import commands
import json
import subprocess
import sys
import traceback
import os
import re
import time
import threading
import asyncio
from termcolor import colored

#############
# Fonctions #
#############

# Préfixe
def prefixe(bot, message):
    with open("config.json", "r") as fichier:
        config = json.loads(fichier.read())
        try:
            return config[str(message.guild.id)]["prefixe"]
        except:
            return "&"

# Traductions
def getmsg(ctx, txt):

    with open("config.json", "r") as fichier:
        config = json.loads(fichier.read())

    try:
        return trad[config[str(ctx.message.guild.id)]["lang"]][txt]
    except:
        return ""

#############
# Variables #
#############

bot = commands.Bot(command_prefix=prefixe)

# Secrets
with open("secrets.json", "r") as fichier:
        secrets = json.loads(fichier.read())

# Config
defaultConfig = \
{"prefixe": "&",
"lang": "en"}

# Traductions
with open("trads.json", "r") as fichier:
    trad = json.loads(fichier.read())

##############
# Coroutines #
##############

bot.remove_command("help")

# On ready
@bot.event
async def on_ready():

        # Moi
        global thedevkiller

        thedevkiller = await bot.get_user_info(436105272310759426)

        print(colored("Je suis connecté !", "white"))

        # Présence
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(name="&help", type=discord.ActivityType.listening), afk=False)
        
        # Charger les cogs
        for fichier in os.listdir("cogs"):
            if re.match(r".*\.py.swp", fichier):
                pass
            elif re.match(r".*\.py", fichier):
                print(colored(f"Chargement de {fichier}", "white"))
                bot.load_extension("cogs." + fichier.replace(".py", ""))

        # Chargement de la config
        with open("config.json", "r") as fichier:
            config = json.loads(fichier.read())

        # Config par défaut
        for server in bot.guilds:
            if str(server.id) in config:
                for param in defaultConfig:
                    if not param in config[str(server.id)]:
                        config[str(server.id)][param] = defaultConfig[param]
            else:
                config[str(server.id)] = defaultConfig
        with open("config.json", "w") as fichier:
            fichier.write(json.dumps(config, indent=4))

        # Séparateur
        print("------------")

# Halt
@bot.command(name="halt", aliases=["shutdown"])
async def halt(ctx):
        if ctx.message.author == thedevkiller:
            with open("config.json", "r") as fichier:
                config = json.loads(fichier.read())
            await ctx.send(getmsg(ctx, "shutdown"))
            sys.exit(0)
        else:
                await ctx.send(trad[config[str(ctx.message.guild.id)]["lang"]]["youcant"])

# Reboot
@bot.command(name="reboot", usage="reboot")
async def reboot(ctx):
        if ctx.message.author == thedevkiller:
                print("Je redémarre")
                await ctx.send(getmsg(ctx, "rebootmsg"))
                subprocess.call(["bash", "/home/thedevkiller/TheBotKiller/reboot.sh"])
                sys.exit(0)
        else:
                await ctx.send(getmsg(ctx, "youcant"))
        
# Load        
@bot.command(name="load", aliases=["charge"])
async def load(ctx, arg):
        if ctx.message.author == thedevkiller:
                try:
                        bot.load_extension("cogs." + arg)
                        await ctx.send(getmsg(ctx, "loaded").format(arg))  
                except ModuleNotFoundError:
                    await ctx.send(getmsg(ctx, "idonthavemodule"))
        else:
                await ctx.send(getmsg(ctx, "youcant"))

# Reload
@bot.command(name="reload", aliases=["recharge"])
async def reload(ctx, arg):
        if ctx.message.author == thedevkiller:
                try:
                        bot.unload_extension("cogs." + arg)
                        bot.load_extension("cogs." + arg)
                        await ctx.send(getmsg(ctx, "reloaded").format(arg))
                except ModuleNotFoundError:
                        await ctx.send(getmsg(ctx, "idonthavemodule"))
        else:
                await ctx.send(getmsg(ctx, "youcant"))

# Unload
@bot.command(name="unload", aliases=["décharge"])
async def unload(ctx, arg):
        if ctx.message.author == thedevkiller:
                try:
                        bot.unload_extension("cogs." + arg)
                        await ctx.send(getmsg(ctx, "unloaded").format(arg))
                except ModuleNotFoundError:
                        await ctx.send(getmsg(ctx, "unloaded"))
        else:
                await ctx.send(getmsg(ctx, "youcant"))

# Erreurs
@bot.event
async def on_error(event, *args, **kwargs):

    try:
        message = args[0]
        await message.channel.send("An error happened, </TheDevKiller>#8230 has been notified")

    except:
        pass

    try:
        commande = message.content.split(" ")[0]
    except: 
        commande = " "

    err = traceback.format_exc()
    
    print(colored(err, "red"))

## Cogs chargées
#@commands.command(name="cogs", aliases=["modules"], brief="Liste des modules")
#async def cogs(ctx):

# Config
@bot.command(aliases=["config"], usage="(conf|config) setting value")
async def conf(ctx, param, valeur):

    if param in defaultConfig:
        with open("config.json", "r") as fichier:
            config = json.loads(fichier.read())

        config[str(ctx.message.guild.id)][param] = valeur

        with open("config.json", "w") as fichier:
            fichier.write(json.dumps(config, indent=4))

    else:
        await ctx.send(getmsg(ctx, "noavailableset"))

# Help
@bot.command(aliases=["aide"], usage="(help|aide)")
async def help(ctx, arg="defaultarg"):

    if arg == "defaultarg":

        dico = {}

        em = discord.Embed(title=getmsg(ctx, "helptitlembed"), color=0xff0000)

        for commande in bot.commands:

            if commande.hidden == False:

                if not commande.cog_name in dico:

                    dico[commande.cog_name] = []

                dico[commande.cog_name].append(f"`{commande.name}`: {getmsg(ctx, commande.name)}")

        for index, categorie in enumerate(dico):

            if categorie == None:

                em.add_field(name="Main", value="\n".join(dico[categorie]))

            else:

                em.add_field(name=categorie, value="\n".join(dico[categorie]))

            em.set_footer(text=getmsg(ctx, "helpembedfooter"))

        await ctx.send(embed=em)

    else:

        for commande in bot.commands:

            if commande.name == arg:

                em = discord.Embed(title=commande.name.capitalize(), description=getmsg(ctx, commande.name), color=0xff0000)

                if commande.aliases != []:

                    em.add_field(name="Aliases", value=", ".join(commande.aliases))

                if isinstance(commande.usage, str):

                    n = "\n"

                    em.add_field(name="Usage", value=f"`\n{command.usage}\n`")

                if isinstance(commande.cog_name, str):

                    em.add_field(name="Category", value=commande.cog_name)

                await ctx.send(embed=em)

# Input
async def handle_console_input():
    while not bot.is_closed():
        console_input = await bot.loop.run_in_executor(None, input, "")
        bot.dispatch("console_input", console_input)

bot.loop.create_task(handle_console_input())

@bot.event
async def on_console_input(input):
    if input.split(" ")[0] == "dis":

                serveurid = int(input.split(" ")[1])
                serveur = bot.get_guild(serveurid)

                channelid = int(input.split(" ")[2])
                channel = serveur.get_channel(channelid)

                string = " ".join(input.split(" ")[3:])
                await channel.send(string)
    elif input.split(" ")[0] == "exit":
        sys.exit(0)

# Logs
@bot.event
async def on_command(ctx):
    print(colored(f"[COMMAND][{time.asctime()}]: {ctx.message.content}, {ctx.message.author.name}, {ctx.message.guild}", "white"))

bot.run(secrets["token"])
