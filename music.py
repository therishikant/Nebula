import discord
from discord.ext import commands
import youtube_dl


from song import Song
from scheduler import Scheduler

class music(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.scheduler = None

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
      await ctx.send("There is no song in the queue to be paused")

  @commands.command()
  async def resume(self, ctx):
    if self.scheduler != None:
      self.scheduler.resumeSong()
      await ctx.send("resumed ▶️")
    else:
      await ctx.send("There is no song in the queue to be paused")
  
  @commands.command()
  async def next(self, ctx):
    if self.scheduler != None:
      self.scheduler.playNextSong()
      await ctx.send("Next Song▶️")
    else:
      await ctx.send("There is no song in the queue.")

  @commands.command()
  async def previous(self, ctx):
    if self.scheduler != None:
      self.scheduler.playPreviousSong()
      await ctx.send("Previous Song▶️")
    else:
      await ctx.send("There is no song in the queue.")

  @commands.command()
  async def p(self,ctx,url):
    print("Received request to play a song")
    if self.scheduler == None:
      print("Scheduler is unavialabel creating a anew one")
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
    self.scheduler.addToQueue()

    print("There is/are now"+ str(self.scheduler.getQueueLength()) +" song(s) in the queue to be paused")
    await ctx.send("There is/are now"+ str(self.scheduler.getQueueLength()) +" song(s) in the queue to be paused")
      
      
    
def setup(client):
  client.add_cog(music(client))
  

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  YDL_OPTIONS = {'format': 'bestaudio', 'forceduration': True}

  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(url, download = False)
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
    return Song(ctx, source, self.client, info['duration'])
