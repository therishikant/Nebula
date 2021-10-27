from song import Song
from threading import Thread

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

  def shuffleQueue():
    pass

  def playPreviousSong(self):
    if (self.previousSong != None):
      currentSong = self.getCurrentSong()
      if currentSong != None:
        currentSong.stopPlaying()
        currentSong.songState = Song.SongState.NOT_STARTED
      self.previousSong.songState = Song.SongState.NOT_STARTED
      self.songQueue.insert(0, self.previousSong)
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
      self.songQueue.pop(0)
      self.previousSong = currentSong

  def getCurrentSong(self):
    if (len(self.songQueue) >= 0):
      return self.songQueue[0]
    return None



  def run(self):
    while True:
      song = self.getSongFromQueue()
      print("Found song with state: ", song.songState)
      while (song.songState != Song.SongState.END):
        if (song.songState == Song.SongState.NOT_STARTED):
          song.startPlaying()
        if (song.songState == Song.SongState.PLAYING):
          self.checkForSongEnd(song)
        time.sleep(2)
        
        


  