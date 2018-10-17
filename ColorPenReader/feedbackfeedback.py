import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import pulseio
import time
import array

class RotaryEncoder:

    __oldAB = None
    encoderPos = 0
    channelA = None
    channelB = None 
    isNewValue = False

    def __init__(self, channelAPin, channelBPin):
        self.channelA = AnalogIn(channelAPin)
        self.channelB = AnalogIn(channelBPin)

        self.encoderPos = 0
        self.isNewValue = False

    def isNewVal(self):
        return self.isNewValue

    def readPinA(self):
        val = (self.channelA.value * 3.3) / 65536
        if val > 0.05:
            return 1
        else: return 0

    def readPinB(self):
        val = (self.channelB.value * 3.3) / 65536
        if val > 0.05:
            return 1
        else: return 0

    def readEncoder(self):
        return self.encoderPos

    def updateEncoder(self):
        enc_states = [0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0]

        if(self.__oldAB == None):
            self.__oldAB = ((self.readPinA() << 1) | self.readPinB())

        self.__oldAB = (self.__oldAB << 2) & 0x0f

        __encodervalues = ((self.readPinA() << 1) | self.readPinB())
        self.__oldAB |= (__encodervalues & 0x03)
  
        if(enc_states[( self.__oldAB & 0x0f )] == 0):
            self.isNewValue = False
        else:
            self.isNewValue = True

        self.encoderPos = (self.encoderPos + enc_states[( self.__oldAB & 0x0f )]) % 3

isScanning = DigitalInOut(board.D1)
isScanning.direction = Direction.INPUT
isScanning.pull = Pull.UP

RPIReady = DigitalInOut(board.D2)
RPIReady.direction = Direction.INPUT
RPIReady.pull = Pull.UP

updateEncoderPWM = pulseio.PWMOut(board.D0, duty_cycle = 2 ** 15, frequency = 50000)
updateEncoder = pulseio.PulseOut(updateEncoderPWM) # create a pulsetrain on D1
pulse = array.array('H', [10, 10]) # define pulsetrain as a HIGH pulse of 20 us
encoder = RotaryEncoder(board.D3, board.D4)

while(True):
    while RPIReady.value:   #using pullups, so logic is inverted
        time.sleep(0.1) # busy wait; change to interrupt to conserve power?
    while not isScanning.value:    #using pullups, so logic is inverted
        encoder.updateEncoder()
        if ( (encoder.readEncoder() == 0) and (encoder.isNewVal()) ): # after one detent pulseout
            updateEncoder.send(pulse)
