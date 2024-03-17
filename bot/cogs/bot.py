from io import BytesIO
import os
from aiohttp import ClientSession
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import datetime
import random
from PIL import Image
import requests

name = 'Wyvern'
tag = '11208'
puuid = 'a756a896-b856-5cd2-8695-235816d4324b'
DELAY = 60


async def asyncGetInfo(call, session):
    async with session.get(call) as response:
        result = await response.json()
        return result

class Bot(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel = None
        self.match_id = None
        self.mutewolfymobile = False
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if (message.author.id == 340590217658630144):
            if (random.randint(0, 1000) == 420):
                await message.channel.send("YOU ARE TERRIBLE NEBERMINDOW")
            if (message.author.mobile_status != discord.Status.offline and self.mutewolfymobile):
                await message.delete()
        if (message.author.bot == False and random.randint(0, 10000) == 420):
            base_image = Image.open('big_thumb.png')
            response = requests.get(message.author.display_avatar)
            if response.status_code == 200:
                try:
                    overlay_image = Image.open(BytesIO(response.content))
                    overlay_image = overlay_image.resize((125,125))
                    base_image.paste(overlay_image, (25,35))
                    base_image.paste(overlay_image, (25,300))
                    base_image.paste(overlay_image, (25,580))
                    base_image.save('./bot/cogs/temp/output.png')
                    await message.reply(file=discord.File('./bot/cogs/temp/output.png'))
                    os.remove('./bot/cogs/temp/output.png')
                except Exception as e:
                    print(e)
                    await message.channel.send("Failed, please ping cygnus this should not have happened...")
            else:
                print("Failed to download the image")
                await message.channel.send("Failed, please ping cygnus this should not have happened...")

    #what gets run when the bot starts
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"YOU ARE TERRIBLE NEBERMINDOW"))
        print('This bot is online!')
        while True:
            if self.channel != None:
                async with ClientSession() as session:
                    c = await asyncGetInfo(f'https://api.henrikdev.xyz/valorant/v3/matches/na/{name}/{tag}', session)
                    try:
                        players = c['data'][0]['players']['all_players']
                    except Exception as e:
                        print("**--- Problem ---**")
                        print(e)
                        print(players)
                        await asyncio.sleep(DELAY)
                        continue
                    map = c['data'][0]['metadata']['map']
                    if (self.match_id == c['data'][0]['metadata']['matchid']):
                        await asyncio.sleep(DELAY)
                        continue
                    if (c['data'][0]['metadata']['mode'].lower() != 'competitive'):
                        await asyncio.sleep(DELAY)
                        continue
                    self.match_id = c['data'][0]['metadata']['matchid']
                    for player in players:
                        if player['puuid'] == puuid:
                            team = player['team'].lower()
                            if (c['data'][0]['teams'][f'{team}']['has_won']):
                                break
                            dmg_per_round = int(player['damage_made']/c['data'][0]['metadata']['rounds_played'])
                            embed = discord.Embed(
                                title = f":biohazard: Loss detected for {name}#{tag} on {map} :biohazard:",
                                description= f"> **Rank:** {player['currenttier_patched']}\n > **Dmg Per Round:** {dmg_per_round}\n > **Match Length:** {datetime.timedelta(seconds=c['data'][0]['metadata']['game_length'])}",
                                color = discord.Color.red()
                            )
                            embed.set_thumbnail(url=player['assets']['agent']['small'])
                            if (player['stats']['kills']/player['stats']['deaths'] > 1):
                                emoji = ":thinking:"
                            else:
                                emoji = ":skull:"
                            embed.add_field(name=f"KDA {emoji}", value=f"> {player['stats']['kills']}/{player['stats']['deaths']}/{player['stats']['assists']}", inline=True)
                            embed.set_footer(text=f"Mode: {c['data'][0]['metadata']['mode']}")
                            await self.channel.send(embed=embed) 
                            break
            await asyncio.sleep(DELAY)

    #help command
    @app_commands.command(name= 'setchannel', description = 'Sets the current channel')
    async def help(self, interaction: discord.Interaction) -> None:
        self.channel = interaction.channel
        await interaction.response.send_message("Channel set to " + self.channel.name, ephemeral=True)
    
    @app_commands.command(name= 'unset', description = 'Stops the updating')
    async def unset(self, interaction: discord.Interaction) -> None:
        self.channel = None
        await interaction.response.send_message("Channel unset", ephemeral=True)

    @app_commands.command(name='mutenevermindmobile', description='mutes nevermind mobile')
    async def mutenevermindmobile(self, interaction: discord.Interaction) -> None:
        self.mutewolfymobile = not(self.mutewolfymobile)
        await interaction.response.send_message(f"Set nevermind mobile blocking to {self.mutewolfymobile}", ephemeral=True)

    @app_commands.command(name='gamingfriday', description='gets the amount of time till next gaming friday')
    async def gamingfriday(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        events = await interaction.guild.fetch_scheduled_events()
        start_time = None
        for event in events:
            if "friday" in event.name.lower():
                start_time = event.start_time
                break
        if not start_time:
            await interaction.followup.send("No gaming friday found", ephemeral=True)
            return
        informal_time = f'<t:{int(start_time.timestamp())}:R>'
        formal_time = f'<t:{int(start_time.timestamp())}:F>'
        description = f"""The next **GAMING FRIDAY** will take place on {formal_time}\n> Which is {informal_time} see you soon!\n"""
        embed = discord.Embed(
            title = f":exclamation: GAMING FRIDAY :exclamation:",
            description = description,
            color = discord.Color.from_str("#2F3136")
        )
        user_list = ''
        async for user in event.users():
            user_list += f"{user.mention}\n"
        if user_list == '':
            user_list = "No one yet :("
        embed.add_field(name="Current list of people attending: ", value=user_list, inline=True)
        await interaction.followup.send(embed=embed, ephemeral=True)
    


async def setup(bot: commands.Bot):
    await bot.add_cog(Bot(bot))
