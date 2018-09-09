###########
# Imports #
###########

import discord
from discord.ext import commands
import os
import subprocess
import re
import psutil
import speedtest
import json

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

#############
# Variables #
#############


########
# Code #
########

class Infos:
        
        def __init__(self, bot):
                self.bot = bot
                self.speedtestEnCours = False
        
        # Code source
        @commands.command(alias=["source", "github"], usage="(code|source|github)")
        async def code(self, ctx):
            with open("config.json", "r") as fichier:
                config = json.loads(fichier.read())
            await ctx.send("https://github.com/TheDevKiller/TheBotKiller")

        # PC 
        @commands.command(usage="pc (infos|hardware)")
        async def pc(self, ctx, arg):
            
            # Config
            with open("config.json", "r") as fichier:
                global config
                config = json.loads(fichier.read())
            
            # Infos
            if arg == "infos":

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

                                # Stockage
                        st = os.statvfs("/")
                        used = round((st.f_blocks - st.f_bfree) * st.f_frsize / 1000000000, 1)
                        total = round(st.f_blocks * st.f_frsize / 1000000000, 1)

                                # Color
                        if float(la.split(" ")[0].replace("**", "")) <= 3: color = 0x00ff00
                        elif float(la.split(" ")[0].replace("**", "")) > 3 and float(la.split(" ")[0].replace("**", "")) < 4: color = 0xFF6D00
                        elif float(la.split(" ")[0].replace("**", "")) >= 4: color = 0xff000
                        else: color = 0xffffff

                                # Batterie
                        btoutput = subprocess.check_output(["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT1"]).decode()
                        batterie = re.search("percentage:          (.{1,3})%", btoutput)[1]
                        em = discord.Embed(title=getmsg(ctx, "titlepcinfosembed"), color=color)
                        em.add_field(name="<:level_slider:474325122904489984> Load Average", value=la) # Load Average
                        em.add_field(name="<:cpu:452823427137667089> CPU", value="**" + str(psutil.cpu_percent()) + "%**") # CPU Percent
                        em.add_field(name="<:computerram:452824190475698187> RAM", value="**" + str(psutil.virtual_memory().percent) + "% **") # RAM Percent
                        #uptimeEmoteNbre = subprocess.check_output("uptime").split(" ")[3]
                        if config[str(ctx.message.guild.id)]["lang"] == "fr":
                            em.add_field(name=":clock10: Uptime", value="**" + uptimep.replace("week", "semaine").replace("day","jour").replace("hour","heure") + "**")
                        elif config[str(ctx.message.guild.id)]["lang"] == "en":
                            em.add_field(name=":clock10: Uptime", value="**" + uptimep+ "**")
                        em.add_field(name="<:ubuntu:465194164548665345> OS", value="**Ubuntu 18.04 LTS**") # OS
                        em.add_field(name=getmsg(ctx, "usedspace"), value="**" + str(used) + "**" + "/" + "**" + str(total) + "** GB")
                        em.add_field(name=getmsg(ctx, "batterynamembed"), value="**" + batterie + "**%")
                        await ctx.send(embed=em)
                                
            # Hardware
            elif arg == "hardware":
                                
                        em = discord.Embed(title=getmsg(ctx, "titlepchardembed"), color=0x106b02)
                        em.add_field(name=getmsg(ctx, "pcmodel"), value="**MSI CX62 6QD 249XFR**")
                        em.add_field(name="<:nvidia:474722211391995904> GPU", value="**NVIDIA 940MX 2**GB")
                        em.add_field(name="<:intel:474722665752428569> CPU", value="**Intel core i3 2 coeurs**")
                        em.add_field(name="<:computerram:452824190475698187> RAM", value="**4GB DDR4**")
                        em.add_field(name=getmsg(ctx, "pcscreen"), value="**Mat 1366**x**768** **15**.**6**\" **16**:**9**")
                        em.add_field(name=getmsg(ctx, "batterynamembed"), value="**Lithium**-**ion**")
                        em.add_field(name=getmsg(ctx, "pchdd"), value="**HDD 500**GB")

                        await ctx.send(embed=em)

            else:
                        await ctx.send(getmsg(ctx, "commandusage").format(ctx.command.usage))

        # Serveurs
        @commands.command(aliases=["serveurs"], usage="(serveurs|servers)")
        async def servers(self, ctx):
            with open("config.json", "r") as fichier:
                config = json.loads(fichier.read())
            serveurs = "** **\n"
            servnbre = 0
            for elements in self.bot.guilds:
                    serveurs += "- " + elements.name + "\n\n"
                    servnbre += 1
            em = discord.Embed(title="<:server:452826125584826378> Serveurs", description=getmsg(ctx, "servs").format(servers=serveurs, servnbre=servnbre), color=0x0294fc)
            await ctx.send(embed=em)

        # Membres
        @commands.command(aliases=["membres"], usage="(membres|members)")
        async def members(self, ctx):
            
            # Config
            with open("config.json", "r") as fichier:
                config = json.loads(fichier.read())
            
            status = \
            {"online": {"False": 0, "True": 0},
            "offline": {"False": 0, "True": 0},
            "idle": {"False": 0, "True": 0},
            "dnd": {"False": 0, "True": 0}}
                        
            # Check du status des membres et du nombre
            for membre in ctx.message.guild.members:
                    status[str(membre.status)][str(membre.bot)] += 1
            
            # Embed
            em = discord.Embed(title=":busts_in_silhouette: Membres", description="Total: **{}**".format(status["online"]["False"] + status["offline"]["False"] + status["idle"]["False"] + status["dnd"]["False"] + status["online"]["True"] + status["offline"]["True"] + status["idle"]["True"] + status["dnd"]["True"]), color=0x6817ff)
            em.add_field(name=":robot: Bots", value="Total: **{total}**\nEn ligne: **{online}**\nNe pas déranger: **{dnd}**\nInactif: **{idle}**\nHors ligne: **{offline}**".format(total=status["online"]["True"] + status["offline"]["True"] + status["idle"]["True"] + status["dnd"]["True"], online=status["online"]["True"], offline=status["offline"]["True"], idle=status["idle"]["True"], dnd=status["dnd"]["True"]))
            em.add_field(name=":raising_hand: Humains", value="Total: **{total}**\nEn ligne: **{online}**\nNe pas déranger: **{dnd}**\nInactif: **{idle}**\nHors ligne: **{offline}**".format(total=status["online"]["False"] + status["offline"]["False"] + status["idle"]["False"] + status["dnd"]["False"], online=status["online"]["False"], offline=status["offline"]["False"], idle=status["idle"]["False"], dnd=status["dnd"]["False"]))
        
            await ctx.send(embed=em)

        # Speedtest
        @commands.command(usage="speedtest")
        async def speedtest(self, ctx):

            # Config
            with open("config.json", "r") as fichier:
                config = json.loads(fichier.read())

            # Speedtest
            if self.speedtestEnCours == False:
                    speedtestEnCours = True

                    messageChargement = await ctx.send(getmsg(ctx, "searchspeedserv"))

                    # Speedtest
                    test = speedtest.Speedtest()
                    
                    # Obtenir le meilleur serveur
                    test.get_best_server()

                    await messageChargement.edit(content = getmsg(ctx, "measuringdownload"))

                    # Test du Download
                    test.download()

                    await messageChargement.edit(content = getmsg(ctx, "measuringupload"))
                    
                    # Test de l'upload
                    test.upload()
                    
                    # URL de l'image
                    url = test.results.share()

                    await messageChargement.delete()
                    
                    # Embed
                    em = discord.Embed(color=0x012ea0)
                    em.set_image(url=test.results.share())
                    
                    await ctx.send(embed=em)
                    
                    speedtestEnCours = False

        # Avatar
        @commands.command(aliases=["pp"], usage="(avatar|pp) mention")
        async def avatar(self, ctx, user:discord.Member):
            try:
                await ctx.send(f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png?size=2048")
            except:
                await ctx.send(getmsg(ctx, "erroravatar"))

def setup(bot):
        bot.add_cog(Infos(bot))
