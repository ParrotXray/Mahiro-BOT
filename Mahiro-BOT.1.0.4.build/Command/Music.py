import discord
from discord.ext import commands
import random
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from discord.commands import slash_command
from discord import option
from definition.Classes import Cog_Extension
from datetime import datetime
from functools import partial
from discord.ui import Button,View
import youtube_dl
from youtube_dl import YoutubeDL

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdlopts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'dump_single_json': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.thumbnail = data.get('thumbnail')
        self.duration = data.get('duration')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False,bot):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        if 'duration' in data:
            duration = datetime.fromtimestamp(data['duration']).strftime('%M:%S')  # ????????????????????????:???????????????
        else:
            duration = None

        if 'thumbnail' in data:
            # ???????????????????????????
            thumbnail_url = data['thumbnail']
        else:
            thumbnail_url = None

        embed = discord.Embed(title="", description=f"**???????????????** [{data['title']}]({data['webpage_url']}) [{ctx.author.mention}]", color=0xFC85C3, timestamp=datetime.now())
        embed.set_footer(text="Mahiro-BOT",icon_url=bot.user.avatar.url)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        if duration:
            embed.add_field(name='??????', value=f"**`00:00 ??????????????????????????????????????????????????????????????????????????????????????????????????? {duration}`**", inline=True)  # ??? Embed ?????????????????????
        await ctx.respond(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)

class task(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    @discord.ui.button(label='',style=discord.ButtonStyle.blurple, emoji='??????')
    async def Bpause(self, button, interaction):
            """Pause the currently playing song."""
            vc = interaction.guild.voice_client

            if not vc or not vc.is_connected():
                embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
                return await interaction.response.send_message(embed=embed)
            elif not vc.is_playing():
                embed = discord.Embed(title="", description="?????????????????????????????????", color=0xFC85C3)
                return await interaction.response.send_message(embed=embed)
            elif vc.is_paused():
                return

            vc.pause()
            await interaction.response.send_message("?????? ??????")

    @discord.ui.button(label='',style=discord.ButtonStyle.blurple, emoji='??????')
    async def Bresume(self, button, interaction):
        vc = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await interaction.response.send_message(embed=embed)
        elif vc.is_playing():
            embed = discord.Embed(title="", description="????????????", color=0xFC85C3)
            return await interaction.response.send_message(embed=embed)
        elif not vc.is_paused():
            embed = discord.Embed(title="", description="?????????????????????????????????", color=0xFC85C3)
            return await interaction.response.send_message(embed=embed)

        vc.resume()
        await interaction.response.send_message("?????? ??????")

    @discord.ui.button(label='',style=discord.ButtonStyle.blurple, emoji='???')
    async def Bskip(self, button, interaction):
        vc = interaction.guild.voice_client
        """Skip the song."""

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await interaction.response.send_message(embed=embed)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            embed = discord.Embed(title="", description="?????????????????????????????????", color=0xFC85C3)
            return await interaction.response.send_message(embed=embed)

        await interaction.response.send_message("?????????????????? ???")
        vc.stop()
        
    @discord.ui.button(label='',style=discord.ButtonStyle.grey, emoji='????')
    async def Bavolume(self, button, interaction):
        vc = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await interaction.response.send_message(embed=embed)
        elif not vc.is_playing():
            embed = discord.Embed(title="", description="?????????????????????????????????", color=0xFC85C3)
            return await interaction.response.send_message(embed=embed)

        current_volume = vc.source.volume * 100
        if current_volume == 100:
            embed = discord.Embed(title="", description="???? **????????????**", color=0xFC85C3)
        else:
            new_volume = current_volume + 10
            if new_volume > 100:
                new_volume = 100
            vc.source.volume = new_volume / 100
            embed = discord.Embed(title="", description=f'**`{interaction.user}`** **??????????????? {new_volume}%**', color=0xFC85C3)
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label='',style=discord.ButtonStyle.grey, emoji='????')
    async def Bbvolume(self, button, interaction):
        vc = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await interaction.response.send_message(embed=embed)
        elif not vc.is_playing():
            embed = discord.Embed(title="", description="?????????????????????????????????", color=0xFC85C3)
            return await interaction.response.send_message(embed=embed)

        current_volume = vc.source.volume * 100
        if current_volume == 0:
            embed = discord.Embed(title="", description="???? **????????????**", color=0xFC85C3)
        else:
            new_volume = current_volume - 10
            if new_volume < 0:
                new_volume = 0
            vc.source.volume = new_volume / 100
            embed = discord.Embed(title="", description=f'**`{interaction.user}`** **??????????????? {new_volume}%**', color=0xFC85C3)
        await interaction.response.send_message(embed=embed)

class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'??????????????????????????????\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed = discord.Embed(title="????????????", description=f"[{source.title}]({source.web_url}) [{source.requester.mention}]", color=0xFC85C3, timestamp=datetime.now())
            embed.set_footer(text="Mahiro-BOT",icon_url=self.bot.user.avatar.url)
            if source.thumbnail:
                embed.set_thumbnail(url=source.thumbnail)
            if source.duration:
                duration = datetime.fromtimestamp(source.duration).strftime('%M:%S')
                embed.add_field(name='??????', value=f"**`00:00 ??????????????????????????????????????????????????????????????????????????????????????????????????? {duration}`**", inline=True)  # ??? Embed ?????????????????????
            self.np = await self._channel.send(embed=embed,view=task(self.bot))
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now()
        day=now.strftime("%Y-%m-%d %H:%M:%S")
        print (f'{day}-Music?????????')

    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('????????????????????????????????????')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('??????????????????????????????'
                           '?????????????????????????????????????????????????????????')

        print('???????????? {} ???????????????'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @slash_command(name="??????-????????????", description="????????????")
    #@commands.command(name='join', aliases=['connect', 'j'], description="connects to voice")
    async def connect_(self, ctx):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        channel: discord.VoiceChannel=None

        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                embed = discord.Embed(title="", description="????????????????????????", color=0xFC85C3)
                await ctx.respond(embed=embed)
                raise InvalidVoiceChannel('???????????????????????? ???????????????????????????????????????????????????')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                embed = discord.Embed(title="", description="?????????????????????", color=0xFC85C3)
                await ctx.respond(embed=embed)
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'??????????????????<{channel}>?????????')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'??????????????????<{channel}>?????????')

        await ctx.respond(f'**?????????? `{channel}`**')

        vc = ctx.voice_client
        player = self.get_player(ctx)
        if vc.source:
            vc.source.volume = 100 / 100

        player.volume = 100 / 100

    @slash_command(name="??????-????????????", description="??????????????????????????????")
    #@commands.command(name='play', aliases=['sing','p'], description="streams music")
    async def splay_(self, ctx):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        ?????? = 'https://www.youtube.com/watch?v=wrYF0HX7Kzc'

        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, ??????, loop=self.bot.loop, download=False, bot = self.bot)

        await player.queue.put(source)

    @slash_command(name="??????-??????", description="????????????")
    @option("??????????????????",description="?????????????????????????????????")
    #@commands.command(name='play', aliases=['sing','p'], description="streams music")
    async def play_(self, ctx, *, ??????????????????: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, ??????????????????, loop=self.bot.loop, download=False, bot = self.bot)

        await player.queue.put(source)

    @slash_command(name="??????-????????????", description="??????????????????")
    #@commands.command(name='pause', description="pauses music")
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)
        elif not vc.is_playing():
            embed = discord.Embed(title="", description="?????????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.respond("?????? ??????")

    @slash_command(name="??????-????????????", description="??????????????????")
    #@commands.command(name='resume', description="resumes music")
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)
        elif vc.is_playing():
            embed = discord.Embed(title="", description="????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)
        elif not vc.is_paused():
            embed = discord.Embed(title="", description="?????????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)

        vc.resume()
        await ctx.respond("?????? ??????")

    @slash_command(name="??????-????????????", description="????????????")
    #@commands.command(name='skip', description="skips to next song in queue")
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            embed = discord.Embed(title="", description="?????????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)
        
        vc.stop()
        await ctx.respond('?????????????????? ???')

    @slash_command(name="??????-??????????????????", description="?????????????????????????????????")
    @option("??????",description="?????????????????????")
    #@commands.command(name='remove', aliases=['rm', 'rem'], description="removes specified song from queue")
    async def remove_(self, ctx, ??????: int):
        """Removes specified song from queue"""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)

        player = self.get_player(ctx)
        
        try:
            s = player.queue._queue[??????-1]
            del player.queue._queue[??????-1]
            embed = discord.Embed(title="", description=f"?????? [{s['title']}]({s['webpage_url']}) [{s['requester'].mention}]", color=0xFC85C3)
            await ctx.respond(embed=embed)
        except:
            embed = discord.Embed(title="", description=f'????????????????????? "{??????}"', color=0xFC85C3)
            await ctx.respond(embed=embed)

    @slash_command(name="??????-??????????????????", description="??????????????????")    
    #@commands.command(name='clear', aliases=['clr', 'cl', 'cr'], description="clears entire queue")
    async def clear_(self, ctx):
        """Deletes entire queue of upcoming songs."""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)

        player = self.get_player(ctx)
        player.queue._queue.clear()
        await ctx.respond('???? **?????????**')

    @slash_command(name="??????-????????????", description="????????????")
    #@commands.command(name='queue', aliases=['q', 'playlist', 'que'], description="shows the queue")
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)

        player = self.get_player(ctx)
        if player.queue.empty():
            embed = discord.Embed(title="", description="????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)
        
        seconds = vc.source.duration % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        # Grabs the songs in the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, int(len(player.queue._queue))))

        # Keep track of unique titles
        unique_titles = []

        fmt = ''
        index = 1
        for _ in upcoming:
            title = _['title']
            if title in unique_titles:
                # If title is not unique, add a suffix to the number
                unique_titles.append(title)
            else:
                # If title is unique, add it to the list of unique titles
                unique_titles.append(title)
            fmt += f"`{index}.` [{title}]({_['webpage_url']})\n"
            index += 1

        fmt = f"\n__????????????__:\n[{vc.source.title}]({vc.source.web_url}) | `{duration}`\n\n__?????????:__\n" + fmt + f"\n**{len(upcoming)} ?????????????????????**"
        embed = discord.Embed(title=f'{ctx.guild.name}???????????????', description=fmt, color=0xFC85C3)
        #embed.set_footer(text=f"{ctx.author.display_name}")

        await ctx.respond(embed=embed)

    @slash_command(name="??????-??????????????????", description="???????????????????????????")  
    #@commands.command(name='np', aliases=['song', 'current', 'currentsong', 'playing'], description="shows the current playing song")
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)

        player = self.get_player(ctx)
        if not player.current:
            embed = discord.Embed(title="", description="?????????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)
        
        seconds = vc.source.duration % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        embed = discord.Embed(title="", description=f"[{vc.source.title}]({vc.source.web_url}) [{vc.source.requester.mention}] | `{duration}`", color=0xFC85C3)
        embed.add_field(name = "", value=f"???????????? ????", inline=False)
        #embed.set_author(icon_url=self.bot.user.avatar_url, name=f"Now Playing ????")
        await ctx.respond(embed=embed)

    @slash_command(name="??????-????????????", description="????????????????????????????????????????????????")
    @option("????????????",description="?????????1-100?????????")
    #@commands.command(name='volume', aliases=['vol', 'v'], description="changes Kermit's volume")
    async def change_volume(self, ctx, *, ????????????: float=None):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)
        elif not vc.is_playing():
            embed = discord.Embed(title="", description="?????????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)
        
        if not ????????????:
            embed = discord.Embed(title="", description=f"???? **{(vc.source.volume)*100}%**", color=0xFC85C3)
            return await ctx.respond(embed=embed)

        if not 0 < ???????????? < 101:
            embed = discord.Embed(title="", description="????????????????????? 1 ??? 100 ????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = ???????????? / 100

        player.volume = ???????????? / 100
        embed = discord.Embed(title="", description=f'**`{ctx.author}`** ?????????????????? **{????????????}%**', color=0xFC85C3)
        await ctx.respond(embed=embed)

    @slash_command(name="??????-????????????", description="???????????????????????????????????????")
    #@commands.command(name='leave', aliases=["stop", "dc", "disconnect", "bye"], description="stops music and disconnects from voice")
    async def leave_(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="??????????????????????????????", color=0xFC85C3)
            return await ctx.respond(embed=embed)

        #if (random.randint(0, 1) == 0):
            #await ctx.message.add_reaction('????')
        await ctx.respond('**???? ??????**')

        await self.cleanup(ctx.guild)


def setup(bot):
    bot.add_cog(Music(bot))