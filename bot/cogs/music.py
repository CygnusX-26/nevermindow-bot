import discord
from discord.ext import commands
from discord import app_commands
from typing import cast
import wavelink


async def asyncGetInfo(call, session):
    async with session.get(call) as response:
        result = await response.json()
        return result
    
async def in_VC(voice: discord.VoiceState, interaction: discord.Interaction) -> bool:
    if not voice:
        await interaction.response.send_message("You are not connected to a voice channel")
        return False
    return True

class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name= 'play', description = 'Play a song!')
    async def play(self, interaction: discord.Interaction, query: str) -> None:
        uvoice = interaction.user.voice
        
        if not await in_VC(uvoice, interaction):
            return
        
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            try:
                player = await uvoice.channel.connect(cls=wavelink.Player)
            except Exception as e:
                await interaction.channel.send(f"Failed to connect to the voice channel: {e}")
                return

        if player.channel != uvoice.channel:
            await player.move_to(uvoice.channel)

        player.autoplay = wavelink.AutoPlayMode.partial

        player.home = interaction.channel

        tracks = await wavelink.Playable.search(query)
        if not tracks:
            await interaction.response.send_message("Nothing found :(")
            return
        
        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            await interaction.channel.send(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            await interaction.channel.send(f"Added **`{track}`** to the queue.")

        if not player.playing:
            await player.play(player.queue.get(), volume=30)

        await interaction.response.send_message("Joined your channel")

    @app_commands.command(name= 'queue', description = 'Show the current queue')
    async def queue(self, interaction: discord.Interaction) -> None:
        if not await in_VC(interaction.user.voice, interaction):
            return
        vclient: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not vclient:
            await interaction.response.send_message("I am not connected to a voice channel")
            return
        if not vclient.queue:
            await interaction.response.send_message("The queue is empty")
            return
        queue = vclient.queue
        embed = discord.Embed(title="Queue")
        for i, track in enumerate(queue):
            if i == 10:
                break
            embed.add_field(name=f"{i+1}. {track.title}", value=f"Author: {track.author}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name= 'skip', description = 'Skip the current song')
    async def skip(self, interaction: discord.Interaction) -> None:
        if not await in_VC(interaction.user.voice, interaction):
            return
        vclient: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not vclient:
            await interaction.response.send_message("I am not connected to a voice channel")
            return
        if vclient.playing:
            await vclient.skip(force=True)
            await interaction.response.send_message("Skipped the song")
        else:
            await interaction.response.send_message("The song is not playing bro!")

    @app_commands.command(name= 'pause', description = 'Pause the current song')
    async def pause(self, interaction: discord.Interaction) -> None:
        if not await in_VC(interaction.user.voice, interaction):
            return
        vclient: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not vclient:
            await interaction.response.send_message("I am not connected to a voice channel")
            return
        if not vclient.paused or not vclient.playing:
            await vclient.pause(True)
            await interaction.response.send_message("Paused the song")
        else:
            await interaction.response.send_message("The song is not playing bro!")

    @app_commands.command(name= 'resume', description = 'Resume the current song')
    async def resume(self, interaction: discord.Interaction) -> None:
        if not await in_VC(interaction.user.voice, interaction):
            return
        vclient: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not vclient:
            await interaction.response.send_message("I am not connected to a voice channel")
            return
        if vclient.paused or not vclient.playing:
            await vclient.pause(False)
            await interaction.response.send_message("Resumed the song")
        else:
            await interaction.response.send_message("The song is not paused bro!")

    @app_commands.command(name= 'volume', description = 'Change the volume of the bot')
    async def volume(self, interaction: discord.Interaction, volume: int) -> None:
        if not await in_VC(interaction.user.voice, interaction):
            return
        vclient: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not vclient:
            await interaction.response.send_message("I am not connected to a voice channel")
            return
        if volume < 0 or volume > 100:
            await interaction.response.send_message("Volume must be between 0 and 100")
            return
        await vclient.set_volume(volume)
        await interaction.response.send_message(f"Set the volume to {volume}")

    @app_commands.command(name= 'stop', description = 'Stops the bot and clears the queue')
    async def stop(self, interaction: discord.Interaction) -> None:
        if not await in_VC(interaction.user.voice, interaction):
            return
        vclient: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not vclient:
            await interaction.response.send_message("I am not connected to a voice channel")
            return
        if vclient.queue:
            vclient.queue.clear()
        await vclient.skip()
        await interaction.response.send_message("Stopped!")

    @app_commands.command(name= 'dc', description = 'Disconnect the bot from the voice channel')
    async def disconnect(self, interaction: discord.Interaction) -> None:
        if not await in_VC(interaction.user.voice, interaction):
            return
        vclient: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not vclient:
            await interaction.response.send_message("I am not connected to a voice channel")
            return
        await vclient.disconnect()
        await interaction.response.send_message("Disconnected from the voice channel!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
