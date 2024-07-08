from discord.ext import commands
import discord
import wavelink
class AutoDc ( commands.Cog):
    def __init__ (self, bot: commands.bot):
        self.bot = bot
        self.stackOfPlayersInVc = []

    @commands.Cog.listener()
    async def on_voice_state_update( self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):

        hasLeft = before.channel is not None and after.channel is None
        isBot = member.id == self.bot.user.id

        if (not isBot and hasLeft):
            beforeChannel = before.channel
            if ( len(beforeChannel.members) == 1 and beforeChannel.members[0].id == self.bot.user.id ):
                await before.channel.guild.voice_client.disconnect()
async def setup(bot: commands.Bot):
    await bot.add_cog(AutoDc(bot))
