// Combining heart and breathing

// Reading from serial port for activation code:
// 1: idle
// 2: fixed heart
// 3: beating heart
// nothing otherwise

#include <Adafruit_NeoPixel.h>
// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN            13

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      6

int incomingByte = 0;   // for incoming serial data

// setup the NeoPixel strip
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int delayval = 5; // polling time
int period = 2000; // in ms, period of breathing

int refract = 500;
int P_duration = 100;
int R_duration = 50;
int T_duration = 75;

void setup() {
  Serial.begin(9600);
  pixels.begin(); // This initializes the NeoPixel library.
  pixels.setBrightness(25);// Set maximum overall brightness
}

void turn_off() {
  for (int i = 0; i < NUMPIXELS ; i++) {
    pixels.setPixelColor(i, 0, 0, 0);
  }
}

void idle() {
  // middle pixel
  int led = NUMPIXELS / 2;
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
  pixels.setPixelColor(led, color, color, color);
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
        state = 0;
        time = 0;
      }
      for (int i = led_P_start; i <= led_P_stop; i++) {
        pixels.setPixelColor(i, 255, 0, 0);
      }
      break;
  }
  time = time +  delayval;
}

void loop() {
  // only consider last byte
  // WARNING: if serial port is spammed, will block led update
  while (Serial.available() > 0)
  {
    incomingByte = Serial.read();
  }

  // select mode depending on the last byte read
  switch (incomingByte) {
    case 1:
      idle();
      break;
    case 3:
      beat();
      break;
    default:
      turn_off();
  }

  pixels.show();
  delay(delayval); // Delay for a period of time (in milliseconds).
}

