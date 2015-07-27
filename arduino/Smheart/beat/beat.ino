// one strip of 6 leds, heart beat on 4
// FIXME: not tested with other than 6 leds, leds selection may not be safe

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

int delayval = 25; // polling time
int period = 200; // in ms, period of breathing

int refract = 500;
int P_duration = 100;
int R_duration = 50;
int T_duration = 75;

void setup() {
  pixels.begin(); // This initializes the NeoPixel library.
  pixels.setBrightness(25);// Set maximum overall brightness
}

void turn_off() {
  for (int i = 0; i < NUMPIXELS ; i++) {
    pixels.setPixelColor(i, 0, 0, 0);
  }
}

void beat() {
  turn_off();
  // middle pixel
  int led_wide = NUMPIXELS / 3;
  // P wave
  int led_P_start = floor((NUMPIXELS - 1) / 2);
  int led_P_stop = led_P_start + led_wide - 1;
  // R wave
  int led_R_start = led_wide - 1;
  int led_R_stop =  led_R_start + 2 * led_wide - 1;

  static int time = 0;
  // 0: nothing, 1: P wave, 2: R wave, 3: Twave
  static int state = 0;

  switch (state) {
    case 0:
      if (time >= refract) {
        state++;
        time = 0;
      }
      break;

    case 1:
      if (time >=  P_duration) {
        state++;
        time = 0;
      }
      for (int i = led_P_start; i <= led_P_stop; i++) {
        pixels.setPixelColor(i, 255, 0, 0);
      }
      break;

    case 2:
      if (time >= R_duration) {
        state++;
        time = 0;
      }
      for (int i = led_R_start; i <= led_R_stop; i++) {
        pixels.setPixelColor(i, 255, 0, 0);
      }
      break;
      
    case 3:
      if (time >= T_duration) {
        state=0;
        time = 0;
      }
      for (int i = led_P_start; i <= led_P_stop; i++) {
        pixels.setPixelColor(i, 255, 0, 0);
      }
      break;
  }
  pixels.show();
  delay(delayval); // Delay for a period of time (in milliseconds).
  time = time +  delayval;
}

void loop() {
  beat();
}

