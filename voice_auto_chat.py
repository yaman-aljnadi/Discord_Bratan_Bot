from discord.ext import commands
import random
import subprocess
from inference_discord_test import main
from gtts import gTTS
import os 
import youtube_dl
from discord import Client
import asyncio
import discord




ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

ffmpeg_options = {
    'options': '-vn'
}

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='bot.', description=description)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def in_channel(channel_id):
    def predicate(ctx):
        return ctx.message.channel.id == channel_id
    return commands.check(predicate)


@in_channel(714182716354199562)
@bot.event
async def on_message(message_chat):
    if message_chat.author.id == bot.user.id:
        return
    elif "bot.join" in message_chat.content.lower():
        await bot.process_commands(message_chat)

    elif "bot.mp3" in message_chat.content.lower():
        await bot.process_commands(message_chat)

    elif "bot.auto_chat" in message_chat.content.lower():
        await bot.process_commands(message_chat)

    elif "bot.play" in message_chat.content.lower():
        await bot.process_commands(message_chat)

    elif "bot.stop" in message_chat.content.lower():
        await bot.process_commands(message_chat)

    elif "bot.yt" in message_chat.content.lower():
        await bot.process_commands(message_chat)

    else:
        print(message_chat.content)
        CHAT_BOT = main(message = message_chat.content)
        await message_chat.channel.send(CHAT_BOT)

    guild = message_chat.guild
    # await bot.process_commands(message_chat)
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    # subprocess.call((["espeak", "-w"+"text"+".wav", str(CHAT_BOT)]))
    speach = gTTS(text=CHAT_BOT , lang="en")
    speach.save("good.mp3")

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("good.mp3"))

    voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def join(ctx, *, channel: discord.VoiceChannel):
    """Joins a voice channel"""

    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)

    await channel.connect()

@bot.command()
async def auto_chat(ctx):
    
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(ctx.author.voice.channel.connect())
    await ctx.author.voice.channel.connect()

@bot.command()
async def mp3(ctx, *, query):
    """Plays a file from the local filesystem"""

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(query))

@bot.command()
async def yt(ctx, *, url):
    """Plays from a url (almost anything youtube_dl supports)"""
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(player.title))



@bot.command()
async def play(ctx, *, mytext):
    """Plays a file from the local filesystem"""

    # subprocess.call((["espeak", "-w"+"text"+".wav", mytext]))
    speach = gTTS(text=mytext, lang="no")
    speach.save("good.mp3")

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("good.mp3"))
    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(mytext))

@bot.command()
async def stop(ctx):
    """Stops and disconnects the bot from voice"""

    await ctx.voice_client.disconnect()

# bot.run("NzAyMjQ5NjIxNjMxNTMzMDY5.Xp9Tqg.UNpRatsF_c9l7xAXXfyx1fV-bjA")
bot.run("ODYxNjg2Njc4MjQyNTkwNzQx.YONaQQ.Se_42GHCIEJjqshaW-1aMsMe5NQ")