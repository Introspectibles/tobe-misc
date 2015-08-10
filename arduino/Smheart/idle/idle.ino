// one strip of 6 leds, one in the middle "breathing"

#include <Adafruit_NeoPixel.h>
// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN            13

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      6

int r = 0;

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int delayval = 5; // polling time
int period = 2000; // in ms, period of breathing

void setup() {

  pixels.begin(); // This initializes the NeoPixel library.
  pixels.setBrightness(25);// Set maximum overall brightness
}

void idle() {
  // middle pixel
  int led = NUMPIXELS/2;
  static int time = 0;
  
  static bool up = true;
  
  // inhale / exhale
  if (up) {
    time = time + delayval;
    // time to reverse animation
    if (time >= period) {
      time = period;
      up = false;
    }
  }
  else {
    time = time - delayval;
    if (time <= 0) {
      time = 0;
      up = true;
    }
  }
  
  // compute correspoding color and set it
  int color = map(time, 0, 2000, 0, 255);
  color = constrain(color, 0, 255);
  pixels.setPixelColor(led, color, color,color);
  pixels.show();
  delay(delayval); // Delay for a period of time (in milliseconds).
  
}

void loop() {
  idle();
}
