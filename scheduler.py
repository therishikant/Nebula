from song import Song
from threading import Thread

import random

import time


class Scheduler(Thread):

  songQueue = []
  previousSong = None

  def __init__(self, ctx):
    Thread.__init__(self)
    self.ctx = ctx

  def loopSong(self, song):
    pass

  def clearQueue(self):
    self.songQueue = []

  def addToQueue(self, song):
    self.songQueue.append(song)

  def shuffleQueue(self):
    newSongList = self.songQueue.copy()
    newSongList.pop(0)
    random.shuffle(newSongList)
    self.songQueue = self.songQueue[:1]
    self.songQueue.extend(newSongList)


  def getPreviousSong(self):
    return self.previousSong


########################
  # async def initialiseSong(self, ctx, url, client):
  #   print("Going to initialise song")
  #   FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  #   YDL_OPTIONS = {'format': 'bestaudio', 'forceduration': True}

  #   with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
  #     info = ydl.extract_info(url, download = False)
  #     url2 = info['formats'][0]['url']
  #     source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
  #     return Song(ctx, url, client, source, info['duration'])
###########################

  # async def playPreviousSong(self, ctx, client):
  #   print("######### Previous Song Function Called ##############")
  #   if (self.previousSong != None):
  #     currentSong = self.getCurrentSong()
  #     print("######### Current Song ##############")
  #     if currentSong != None:
  #       currentSong.stopPlaying()
  #       print("######### Current Song Stopped ##############")
  #       currentSong.songState = Song.SongState.NOT_STARTED
      
  #     print("######### Going to initialise previous song ##############")
  #     print(self.previousSong.url)
  #     self.previousSong = await self.initialiseSong(ctx, self.previousSong.url, client)
  #     print("######### Previous Song initialised ##############")
      
  #     print(self.previousSong.songState)
  #     #self.previousSong.songState = self.previousSong.NOT_STARTED
  #     print("######### Previous Song State Set To NOT STARTED ##############")
  #     self.songQueue.insert(0, self.previousSong)
  #     self.previousSong = None
    #     print( "Playing Previous Song")
  #   else:
  #     print("Previous Song Not Found")

  def playPreviousSong(self, previousSong, currentSong):
    if (previousSong != None):
      currentSongPlaying = self.getCurrentSong()
      if currentSongPlaying != None:
        currentSongPlaying.stopPlaying()
      previousSong.songState = Song.SongState.NOT_STARTED
      self.songQueue.insert(0, previousSong)
      if currentSong != None:
        print("Stopping currently playing song: ", currentSong)
        self.songQueue[1] = currentSong
      self.previousSong = None
      print( "Playing Previous Song")
    else:
      print("Previous Song Not Found")
    

  def playNextSong(self):
    currentSong = self.songQueue[0];
    self.previousSong = currentSong
    currentSong.stopPlaying();
    self.songQueue.pop(0)
    print("playing next song")

  # def playQueue(self):
  #   while len(self.songQueue) > 0:
  #     currentSong = self.songQueue[0];
  #     if (currentSong.songState == Song.SongState.NOT_STARTED):
  #       durationOfCurrentSong = currentSong.getDuration()
  #       print(durationOfCurrentSong)
  #       currentSong.startPlaying()
  #       print("Sleep completed.")
  #       currentSong.stopPlaying()
  #       self.previousSong = currentSong
  #       del self.songQueue[0]

  def pauseSong(self):
    print("pausing song")
    currentSong = self.songQueue[0];
    currentSong.pausePlaying();
    
  def resumeSong(self):
    currentSong = self.songQueue[0];
    currentSong.resumePlaying(time.time());

  def getQueueLength(self):
    return len(self.songQueue)

  def getSongFromQueue(self):
    while (len(self.songQueue) <= 0):
      print("No Songs were found in the queue.")
      time.sleep(2)
    print("Found song(s) in the queue: ", len(self.songQueue))
    
    return self.songQueue[0]

  def checkForSongEnd(self, song):
    currentTime = time.time()
    timeLapsed = currentTime - song.startTimeSeconds
    print("song played ", timeLapsed, " seconds out of", song.remainingTime, "seconds")
    if timeLapsed >= song.remainingTime:
      currentSong = self.songQueue[0];
      song.stopPlaying()
      self.previousSong = currentSong

  def getCurrentSong(self):
    if (len(self.songQueue) > 0):
      return self.songQueue[0]
    return None



  def run(self):
    while True:
      song = self.getSongFromQueue()
      if song.songState == Song.SongState.END:
        self.songQueue.pop(0)
      print("Found song with state: ", song.songState)
      while (song.songState != Song.SongState.END):
        if (song.songState == Song.SongState.NOT_STARTED):
          song.startPlaying()
        if (song.songState == Song.SongState.PLAYING):
          self.checkForSongEnd(song)
        time.sleep(2)

      
        
        


  