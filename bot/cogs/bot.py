from io import BytesIO
import os
import discord
from discord.ext import commands
from discord import app_commands
import random
from PIL import Image
import requests

async def asyncGetInfo(call, session):
    async with session.get(call) as response:
        result = await response.json()
        return result

class Bot(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
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

    @app_commands.command(name='mutenevermindmobile', description='mutes nevermind mobile')
    async def mutenevermindmobile(self, interaction: discord.Interaction) -> None:
        self.mutewolfymobile = not(self.mutewolfymobile)
        await interaction.response.send_message(f"Set nevermind mobile blocking to {self.mutewolfymobile}", ephemeral=True)

    
    


async def setup(bot: commands.Bot):
    await bot.add_cog(Bot(bot))
