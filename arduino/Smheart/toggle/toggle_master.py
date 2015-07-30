 
import serial
import struct

input_string = ""

serial_port = "/dev/ttyACM1"
print "Openning: ", serial_port
ard = serial.Serial("/dev/ttyACM1",9600)

while True:
  # read input until EOF
  try:
      input_string = raw_input('> ')
  # catch ctrl-d
  except EOFError:
      print "\nBye!"
      break
  # should be a byte
  try:
    led_state = int(input_string)
  except:
    print "Please enter an integer."
  else:
    if led_state < 0 or led_state > 255:
      print "Command should be between 0 and 255."
    else:
      # send command to arduino
      print "Sending: ", led_state
      st = struct.pack("B",led_state)
      ard.write(st)
      ard.flush()
