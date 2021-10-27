import time

class Song:

  class SongState:
    NOT_STARTED = 0
    PLAYING = 1
    PAUSED = 2
    END = 3

  isLooped = False;

  def __init__(self, ctx, url, client, source, duration):
    self.ctx = ctx
    self.url = url
    self.client = client
    self.songState = self.SongState.NOT_STARTED
    self.source = source
    self.duration = duration
    self.remainingTime = duration
    print("Song with url: ", self.url, " initialised")

  def pausePlaying(self):
    self.ctx.voice_client.pause()
    self.songState = self.SongState.PAUSED
    currentTime = time.time()
    self.reduceDurationTime(currentTime - self.startTimeSeconds)

  def resumePlaying(self, currentTimeSeconds):
    self.startTimeSeconds = currentTimeSeconds
    self.ctx.voice_client.resume()
    self.songState = self.SongState.PLAYING

  def startPlaying(self):
    vc = self.ctx.voice_client
    vc.play(self.source)
    self.remainingTime = self.duration
    self.songState = self.SongState.PLAYING
    self.startTimeSeconds = time.time()

  def stopPlaying(self):
    self.ctx.voice_client.stop()
    self.songState = self.SongState.END

  def resetPlaying(self):
    self.ctx.voice_client.stop()
    print("Resetting song with url: ", self.url)
    self.songState = self.SongState.END


  def setLoop(self, isLooped):
    self.isLooped = isLooped

  def getDuration(self):
    return self.duration

  def reduceDurationTime(self, secondsToReduce):
    self.remainingTime = self.remainingTime - secondsToReduce




  
    

  