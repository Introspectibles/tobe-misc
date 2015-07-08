import numpy
from Tkinter import *

# Compute IBI (for HRV, in seconds) and BPM using stimulations (any type), primery use for heart
# FIXME: all values for one buffer and channel are identical

class MyOVBox(OVBox):
   def __init__(self):
      OVBox.__init__(self)
      self.channelCount = 0
      self.samplingFrequency = 0
      self.epochSampleCount = 0
      self.startTime = 0.
      self.endTime = 0.
      self.dimensionSizes = list()
      self.dimensionLabels = list()
      self.timeBuffer = list()
      self.signalBuffer = None
      self.signalHeader = None
      self.IBIvalue = 1.
      self.BPMvalue = 1./self.IBIvalue*60
      self.lastStimDate = -1
      self.newStimDate = 0

   # this time we also re-define the initialize method to directly prepare the header and the first data chunk
   def initialize(self):
      # one channel for min, another for max
      self.channelCount = 2
           
      # settings are retrieved in the dictionary
      self.samplingFrequency = int(self.setting['Sampling frequency'])
      self.epochSampleCount = int(self.setting['Generated epoch sample count'])
      
      # safeguards (-1 to disable)
      self.minBPM = int(self.setting['Min BPM'])
      self.maxBPM = int(self.setting['Max BPM'])
      # in percentage, max BPM variation between two seconds
      self.maxVariation = int(self.setting['Max variation'])
         
      #creation of the signal header
      self.dimensionLabels.append('IBI') 
      self.dimensionLabels.append('BPM') 
      self.dimensionLabels += self.epochSampleCount*['']
      self.dimensionSizes = [self.channelCount, self.epochSampleCount]
      self.signalHeader = OVSignalHeader(0., 0., self.dimensionSizes, self.dimensionLabels, self.samplingFrequency)
      self.output[0].append(self.signalHeader)

      #creation of the first signal chunk
      self.endTime = 1.*self.epochSampleCount/self.samplingFrequency
      self.signalBuffer = numpy.zeros((self.channelCount, self.epochSampleCount))
      self.updateTimeBuffer()
      self.updateSignalBuffer()
    
   def updateStartTime(self):
      self.startTime += 1.*self.epochSampleCount/self.samplingFrequency

   def updateEndTime(self):
      self.endTime = float(self.startTime + 1.*self.epochSampleCount/self.samplingFrequency)

   def updateTimeBuffer(self):
      self.timeBuffer = numpy.arange(self.startTime, self.endTime, 1./self.samplingFrequency)

   def updateSignalBuffer(self):
      self.signalBuffer[0,:] = self.IBIvalue
      self.signalBuffer[1,:] = self.BPMvalue

   def sendSignalBufferToOpenvibe(self):
      start = self.timeBuffer[0]
      end = self.timeBuffer[-1] + 1./self.samplingFrequency
      bufferElements = self.signalBuffer.reshape(self.channelCount*self.epochSampleCount).tolist()
      self.output[0].append( OVSignalBuffer(start, end, bufferElements) )


   # called by process for each stim reiceived; update timestamp of last stim
   def trigger(self, stim):
     print "Got stim: ", stim.identifier, " date: ", stim.date, " duration: ", stim.duration
     self.newStimDate = stim.date
     self.updateValues()
   
   # called by process each loop or by trigger when got new stimulation;  update IBI/BPM
   def updateValues(self):
     BPMvalue = self.BPMvalue
     # when called by trigger()
     if self.newStimDate != self.lastStimDate:
       BPMvalue = 1./(self.newStimDate - self.lastStimDate)*60
       # safeguard, if too short
       self.lastStimDate = self.newStimDate
       
     # safeguard, if too long
     if self.maxVariation >=0:
       print "laststim", self.lastStimDate, ", new:", self.newStimDate
       nextStim = self.lastStimDate + 1./(BPMvalue-BPMvalue*self.maxVariation/100)*60
       print "nextstim: ", nextStim
       if self.getCurrentTime() >= nextStim:
         self.newStimDate = self.getCurrentTime()
         BPMvalue = 1./(self.newStimDate - self.lastStimDate)*60
         self.lastStimDate = self.newStimDate
         print "safe guard long! ", self.getCurrentTime(), " BPM: ", BPMvalue
     
     # safeguards for min/max
     if self.minBPM >= 0 and BPMvalue < self.minBPM:
       BPMvalue = self.minBPM
     if self.maxBPM >= 0 and BPMvalue > self.maxBPM:
       BPMvalue = self.maxBPM
       
     # update internal state
     self.BPMvalue = BPMvalue
     if self.BPMvalue != 0:
       self.IBIvalue = 1./BPMvalue*60
     else:
       self.IBIvalue = 0
     

   # the process is straightforward
   def process(self):
      ## Deal with received stimulations
      # we iterate over all the input chunks in the input buffer
      for chunkIndex in range( len(self.input[0]) ):
         # if it's a header... we have to catch it otherwise it'll be seen as OVStimulationSet (??), but that's it
         if(type(self.input[0][chunkIndex]) == OVStimulationHeader):
           self.input[0].pop()
         # we reiceive actual data
         elif(type(self.input[0][chunkIndex]) == OVStimulationSet):
           # create a list for corresponding chunck
           stimSetIn = self.input[0].pop()
           # even without any signals we receive sets, have to check what they hold
           nb_stim =  str(len(stimSetIn))
           for stim in stimSetIn:
             # check which 
             self.trigger(stim)
         # useless?
         elif(type(self.input[0][chunkIndex]) == OVStimulationEnd):
           self.input[0].pop()

      ## send IBI & BPM values
      start = self.timeBuffer[0]
      end = self.timeBuffer[-1]
      if self.getCurrentTime() >= end:
         # in case we need to automatically change BPM 'cause of min/max
         self.updateValues()
         # send buffer
         self.sendSignalBufferToOpenvibe()
         self.updateStartTime()
         self.updateEndTime()
         self.updateTimeBuffer()
         self.updateSignalBuffer()

   # this time we also re-define the uninitialize method to output the end chunk.
   def uninitialize(self):
      end = self.timeBuffer[-1]
      self.output[0].append(OVSignalEnd(end, end))

box = MyOVBox()
