/* const int VRxPin = 34;       // joystick X-axis ADC pin
const int VRyPin = 35;       // joystick Y-axis ADC pin
const int buttonPin = 25;    // joystick button pin
const int vibMotorPin = 15;  // vibration motor control pin

const int ADC_CENTER = 2048;
const int DEADZONE = 200;

const int UPPER_THRESHOLD = ADC_CENTER + DEADZONE;
const int LOWER_THRESHOLD = ADC_CENTER - DEADZONE;

bool vibrationActive = false;
bool fallAlertsEnabled = true;
int ultrasonicRange = 100; // starting range in cm

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(vibMotorPin, OUTPUT);
  digitalWrite(vibMotorPin, LOW);
  Serial.println("Joystick control started");
}

void loop() {
  int xVal = analogRead(VRxPin);
  int yVal = analogRead(VRyPin);
  int buttonState = digitalRead(buttonPin);

  if (yVal > UPPER_THRESHOLD) {
    onUp();
  } else if (yVal < LOWER_THRESHOLD) {
    onDown();
  }

  if (xVal > UPPER_THRESHOLD) {
    onRight();
  } else if (xVal < LOWER_THRESHOLD) {
    onLeft();
  }

  if (buttonState == LOW) {
    onPressed();
    delay(300); // debounce delay
  }

  delay(100);
}

void onUp() {
  Serial.print("Current time: ");
  Serial.println(millis() / 1000); // print uptime in seconds
}

void onDown() {
  vibrationActive = !vibrationActive;
  digitalWrite(vibMotorPin, vibrationActive ? HIGH : LOW);
  Serial.print("Vibration motors ");
  Serial.println(vibrationActive ? "ON" : "OFF");
}

void onLeft() {
  ultrasonicRange += 10; // increase range by 10 cm
  if (ultrasonicRange > 500) ultrasonicRange = 500; // limit max
  Serial.print("Ultrasonic range increased to ");
  Serial.print(ultrasonicRange);
  Serial.println(" cm");
}

void onRight() {
  ultrasonicRange -= 10; // decrease range by 10 cm
  if (ultrasonicRange < 10) ultrasonicRange = 10; // limit min
  Serial.print("Ultrasonic range decreased to ");
  Serial.print(ultrasonicRange);
  Serial.println(" cm");
}

void onPressed() {
  fallAlertsEnabled = !fallAlertsEnabled;
  Serial.print("Fall alerts ");
  Serial.println(fallAlertsEnabled ? "ENABLED" : "DISABLED");
}
*/

const int VRxPin = 34;       // Joystick X-axis ADC pin
const int VRyPin = 35;       // Joystick Y-axis ADC pin
const int buttonPin = 25;    // Joystick push button pin

const int ADC_CENTER = 2048;
const int DEADZONE = 200;

const int UPPER_THRESHOLD = ADC_CENTER + DEADZONE;
const int LOWER_THRESHOLD = ADC_CENTER - DEADZONE;

bool vibrationActive = false;
bool fallAlertsEnabled = true;
int ultrasonicRange = 100;   // Starting ultrasonic range in cm

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.println("Joystick control started");
}

void loop() {
  int xVal = analogRead(VRxPin);
  int yVal = analogRead(VRyPin);
  int buttonState = digitalRead(buttonPin);

  if (yVal > UPPER_THRESHOLD) {
    onUp();
  }
  else if (yVal < LOWER_THRESHOLD) {
    onDown();
  }

  if (xVal > UPPER_THRESHOLD) {
    onRight();
  }
  else if (xVal < LOWER_THRESHOLD) {
    onLeft();
  }

  if (buttonState == LOW) {
    onPressed();
    delay(300); // Basic debounce
  }

  delay(100);
}

void onUp() {
  Serial.print("Current time (seconds): ");
  Serial.println(millis() / 1000);
}

void onDown() {
  vibrationActive = !vibrationActive;
  Serial.print("Vibration motors ");
  Serial.println(vibrationActive ? "ON" : "OFF");
}

void onLeft() {
  ultrasonicRange += 10;
  if (ultrasonicRange > 500) ultrasonicRange = 500;
  Serial.print("Ultrasonic range increased to ");
  Serial.print(ultrasonicRange);
  Serial.println(" cm");
}

void onRight() {
  ultrasonicRange -= 10;
  if (ultrasonicRange < 10) ultrasonicRange = 10;
  Serial.print("Ultrasonic range decreased to ");
  Serial.print(ultrasonicRange);
  Serial.println(" cm");
}

void onPressed() {
  fallAlertsEnabled = !fallAlertsEnabled;
  Serial.print("Fall alerts ");
  Serial.println(fallAlertsEnabled ? "ENABLED" : "DISABLED");
}
