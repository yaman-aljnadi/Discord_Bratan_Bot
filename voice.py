import asyncio
import discord
from playsound import playsound
from discord.ext import commands
from discord import Client 
import youtube_dl
from gtts import gTTS
import os
import talkey
import subprocess
from voice_auto_chat import on_message

ffmpeg_options = {
    'options': '-vn'
}


# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get('title')
#         self.url = data.get('url')


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self ,ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    # @commands.command()
    # async def bot_room(self, ctx, message):
    #     if ctx.voice_client is not None:
    #         return await ctx.voice_client.move_to("bot_chat_room")

    #     await channel.connect()

    @commands.command()
    async def MP3(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def play(self, ctx, *, mytext):
        """Plays a file from the local filesystem"""

        subprocess.call((["espeak", "-w"+"text"+".wav", mytext]))
        # speach = gTTS(text= mytext , lang="en-uk")
        # speach.save("text.mp3")

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("text.wav"))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(mytext))


    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

# @bot.event()
# async def auto_chat():
    


bot = commands.Bot(command_prefix=commands.when_mentioned_or("bot."),
                   description='Relatively simple music bot example')



bot.add_cog(Music(bot))
bot.run("NzAyMjQ5NjIxNjMxNTMzMDY5.Xp9Tqg.UNpRatsF_c9l7xAXXfyx1fV-bjA")