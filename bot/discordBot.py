import discord
import os
from discord.ext import commands
import wavelink

class NevermindOWChecker(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("?"),
            description='YOU ARE TERRIBLE NEBERMINDOW',
            intents=discord.Intents.all(),
            application_id = int(os.getenv("APPLICATION_ID")))
        
    async def load_extensions(self) -> None: 
        for filename in os.listdir("bot/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def setup_hook(self) -> None:
        self.remove_command('help')
        nodes = [wavelink.Node(uri="http://host.docker.internal:2333", password="verysecurepassword1234")]
        await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100)

        await self.load_extensions()
        await bot.tree.sync()

    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        print("Wavelink node ready")

    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            return

        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track

        embed: discord.Embed = discord.Embed(title="Now Playing")
        embed.description = f"**{track.title}** by `{track.author}`"

        if track.artwork:
            embed.set_image(url=track.artwork)

        if original and original.recommended:
            embed.description += f"\n\n`This track was recommended via {track.source}`"

        if track.album.name:
            embed.add_field(name="Album", value=track.album.name)
        
        await player.home.send(embed=embed)

bot = NevermindOWChecker()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
