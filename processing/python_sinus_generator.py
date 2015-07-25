 
import numpy

# Sinus generator from OpenViBE tutorial, here we can set the frequency of the mother wave (1st channel), the frequency of others will be a multiple (by 2, 3, and so on).

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

   # this time we also re-define the initialize method to directly prepare the header and the first data chunk
   def initialize(self):
      # settings are retrieved in the dictionary
      self.channelCount = int(self.setting['Channel count'])
      self.samplingFrequency = int(self.setting['Sampling frequency'])
      self.epochSampleCount = int(self.setting['Generated epoch sample count'])
      self.sinusFrequency = float(self.setting['Sinus Frequency'])

      #creation of the signal header
      for i in range(self.channelCount):
         self.dimensionLabels.append( 'Sinus'+str(i) )
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
      # crop number of chunks in case it is not a multiple of frequency
      self.timeBuffer = self.timeBuffer[0:self.epochSampleCount]

   def updateSignalBuffer(self):
      for rowIndex, row in enumerate(self.signalBuffer):
         self.signalBuffer[rowIndex,:] = 100.*numpy.sin( 2.*numpy.pi*(rowIndex+1.)*self.sinusFrequency*self.timeBuffer )

   def sendSignalBufferToOpenvibe(self):
      start = self.timeBuffer[0]
      end = self.timeBuffer[-1] + 1./self.samplingFrequency
      bufferElements = self.signalBuffer.reshape(self.channelCount*self.epochSampleCount).tolist()
      self.output[0].append( OVSignalBuffer(start, end, bufferElements) )

   # the process is straightforward
   def process(self):
      start = self.timeBuffer[0]
      end = self.timeBuffer[-1]
      if self.getCurrentTime() >= end:
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