//Analog pin to connect
#define RUBBERPIN A0

//Average multiple samples to smooth out the readings
#define NUMSAMPLES 5

int samples[NUMSAMPLES];

void setup() {
Serial.begin(9600);

//Connect AREF to 3.3V, less noisy
analogReference(EXTERNAL);
}

void loop() {
	uint8_t i;
	float average;

	//Take N samples in a row, with a slight delay
	for(i = 0; i < NUMSAMPLES; i++) {
		samples[i] = analogRead(RUBBERPIN);
		delay(10);
	}

	//Average the samples
	average = 0;
	for(i = 0; i < NUMSAMPLES; i++) {
		average += samples[i];
	}
	average /= NUMSAMPLES;

	//Output data
	Serial.println(average);
	Serial.println(0);
	delay(50);
}
