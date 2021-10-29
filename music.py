from discord.ext import commands
import youtube_dl
import discord
import validators

from song import Song
from scheduler import Scheduler
from url_fetcher import UrlFetcher

class music(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.scheduler = None

  async def initialiseSong(self, ctx, url):
    print("Going to initialise song")
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio', 'forceduration': True}

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download = False)
      url2 = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
      return Song(ctx, url, self.client, source, info['duration'])

  def getURL(self, searchTerm):
    if validators.url(searchTerm):
      return searchTerm
    return UrlFetcher.getUrl(searchTerm)
    

  @commands.command()
  async def j(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("You're not in a voice channel")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)

  @commands.command()
  async def disconnect(self, ctx):
    await ctx.voice_client.disconnect()

  @commands.command()
  async def pause(self, ctx):
    if self.scheduler != None:
      self.scheduler.pauseSong()
      await ctx.send("Paused ⏸")
    else:
      await ctx.send("There is no song in the queue")

  @commands.command()
  async def resume(self, ctx):
    if self.scheduler != None:
      self.scheduler.resumeSong()
      await ctx.send("Resumed ▶️")
    else:
      await ctx.send("There is no song in the queue")
  
  @commands.command()
  async def next(self, ctx):
    if self.scheduler != None:
      nextSongUrl = self.scheduler.playNextSong()
      await ctx.send("Now Playing " + nextSongUrl)
    else:
      await ctx.send("There is no song in the queue")
  
  @commands.command()
  async def shuffle(self, ctx):
    if self.scheduler != None:
      self.scheduler.shuffleQueue()
      await ctx.send("Song Suffled▶️")
    else:
      await ctx.send("There is no song in the queue")

  @commands.command()
  async def previous(self, ctx):
    if self.scheduler != None and self.scheduler.getPreviousSong() != None:
      prevSong = await self.initialiseSong(ctx, self.scheduler.getPreviousSong().url)
      currentSongObject = self.scheduler.getCurrentSong()
      currentSong = None
      if currentSongObject != None: 
        currentSong = await self.initialiseSong(ctx, self.scheduler.getCurrentSong().url)
      nextSongUrl = self.scheduler.playPreviousSong(prevSong, currentSong)
      await ctx.send("Now Playing " + nextSongUrl)
    else:
      await ctx.send("There is no song in the queue")

  @commands.command()
  async def p(self,ctx, * , url):
    url = self.getURL(url)
    print("Received request to play a song")
    if self.scheduler == None:
      print("Scheduler is unavailable creating a new one")
      self.scheduler = Scheduler(ctx)
      self.scheduler.start()

    
    if ctx.author.voice is None:
      await ctx.send("You're not in a voice channel")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)

    #ctx.voice_client.stop()
    song = await self.initialiseSong(ctx, url)
    print("Song Initalised")
    self.scheduler.addToQueue(song)

    print("There is/are now "+ str(self.scheduler.getQueueLength()) +" song(s) in the queue")
    await ctx.send("There is/are now "+ str(self.scheduler.getQueueLength()) +" song(s) in the queue")
      
      
    
def setup(client):
  client.add_cog(music(client))