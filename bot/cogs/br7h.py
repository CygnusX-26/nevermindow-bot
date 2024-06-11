import discord
from discord.ext import commands
from discord import app_commands

class Br7h(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
    await bot.add_cog(Br7h(bot))
