#include <ESP32Servo.h>
#include <ESP32PWM.h>

Servo myServo;
Servo myServo2;
const int servo1 = 23;// servo2 = 2;
// 15, 2, 0, 4, 5, 16, 17, 5, 18, 19, 23
// 13, 12, 14, 27, 26, 25, 33, 32, 35, 34, 39, 36

// Ultrasonic sensors setup
const int trigPin = 13, echoPin = 12, foreward = 32, backward = 35, pwmPin = 18;
const int trigPin2 = 14, echoPin2 = 27, foreward2 = 33, backward2 = 24, pwmPin2 = 19;
const int trigPin3 = 26, echoPin3 = 25, foreward3 = 15, backward3 = 4, pwmPin3 = 5;
const int radius = 20, radius2 = 20, radius3 = 20;

// Variables for motor control
int pwm = 0,  pwm2 = 0, pwm3 = 0;//servoAngle = 89,

// Variables for timing control
unsigned long servoMillis = 0;
const long servoInterval = 10;  // Time in milliseconds for servo updates

unsigned long sensorMillis = 0;
const long sensorInterval = 100;  // Time in milliseconds for sensor readings

unsigned long printMillis = 0;
const long printInterval = 100;  // Time in milliseconds for serial prints

// Variables for servo control
int servoPos = 0;
bool increasing = true;

// Function to read distance from ultrasonic sensor without blocking
long readDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);  // This is very short and won't cause noticeable blocking
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10); // This is very short and won't cause noticeable blocking
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000); // 30ms timeout to prevent indefinite blocking
  if (duration == 0) return -1; // Timeout occurred
  return duration / 29 / 2;
}

void setup() {
  Serial.begin(115200);
  
  // Servo setup
  myServo.attach(servo1);
  // myServo2.attach(servo2);
  
  // Ultrasonic pins setup
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(foreward, OUTPUT);
  pinMode(backward, OUTPUT);
  pinMode(pwmPin, OUTPUT);

  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(foreward2, OUTPUT);
  pinMode(backward2, OUTPUT);
  pinMode(pwmPin2, OUTPUT);

  pinMode(trigPin3, OUTPUT);
  pinMode(echoPin3, INPUT);
  pinMode(backward3, OUTPUT);
  pinMode(foreward3, OUTPUT);
  pinMode(pwmPin3, OUTPUT);
}

void loop() {

 if (Serial.available()) {
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();  // Remove spaces or newline

  if (cmd == "TIME") {
    Serial.print("Time: ");
    Serial.println(millis() / 1000);
  }
  else if (cmd == "VIB_TG") {
    // Toggle vibration motor ON/OFF globally
    static bool vibrationActive = false;
    vibrationActive = !vibrationActive;
    Serial.print("Vibration motors ");
    Serial.println(vibrationActive ? "ON" : "OFF");
    // You can disable PWM control when off if needed
  }
  else if (cmd == "RANGE_UP") {
    // Increase ultrasonic detection range globally
    radius + 10;
    Serial.print("Ultrasonic range increased to: ");
    Serial.println(radius);
  }
  else if (cmd == "RANGE_DOWN") {
    // Decrease ultrasonic detection range
    radius - 10;
    Serial.print("Ultrasonic range decreased to: ");
    Serial.println(radius);
  }
  else if (cmd == "FALL_OFF") {
    Serial.println("Fall alerts disabled.");
    // Optional: disable fall alert logic if you integrate MPU later
  }
}

  unsigned long currentMillis = millis();
  
  // Update servo positions
  if (currentMillis - servoMillis >= servoInterval) {
    servoMillis = currentMillis;
    
    // Update servo positions
    if (increasing) {
      servoPos++;
      if (servoPos >= 180) {
        increasing = false;
      }
    } else {
      servoPos--;
      if (servoPos <= 0) {
        increasing = true;
      }
    }
    
    // Move servos
    myServo.write(servoPos);
    // myServo2.write(180 - servoPos);
    
    // Update servoAngle for motor control logic
    //servoAngle = servoPos;
  }
  
  // Read sensors and update motors
  if (currentMillis - sensorMillis >= sensorInterval) {
    sensorMillis = currentMillis;
    
    // Read distances from all sensors
    long distance1 = readDistance(trigPin, echoPin);
    long distance2 = readDistance(trigPin2, echoPin2);
    long distance3 = readDistance(trigPin3, echoPin3);
    
    // Control motor 1
    if (distance1 > radius || distance1 < 0) {
      pwm = 0;
      digitalWrite(foreward, LOW);
      digitalWrite(backward, LOW);
      analogWrite(pwmPin, 0);
    } else {
      pwm = map(distance1, 1, radius, 255, 5);
      if (servoPos > 90) {
        digitalWrite(foreward, HIGH);
        digitalWrite(backward, LOW);
        analogWrite(pwmPin, pwm);
      } else {
        digitalWrite(backward, HIGH);
        digitalWrite(foreward, LOW);
        analogWrite(pwmPin, pwm);
      }
    }

    // Control motor 3
    if (distance2 > radius2 || distance2 < 0) {
      pwm2 = 0;
      digitalWrite(foreward2, LOW);
      digitalWrite(backward2, LOW);
      analogWrite(pwmPin2, 0);
    } else {
      pwm2 = map(distance2, 1, radius2, 255, 5);
      if (servoPos > 90) {
        digitalWrite(foreward2, HIGH);
        digitalWrite(backward2, LOW);
        analogWrite(pwmPin2, pwm2);
      } else {
        digitalWrite(backward2, HIGH);
        digitalWrite(foreward2, LOW);
        analogWrite(pwmPin2, pwm2);
      }
    }

    // Control motor 3
    if (distance3 > radius3 || distance3 < 0) {
      pwm3 = 0;
      digitalWrite(foreward3, LOW);
      digitalWrite(backward3, LOW);
      analogWrite(pwmPin3, 0);
    } else {
      pwm3 = map(distance3, 1, radius3, 255, 5);
      if (servoPos > 90) {
        digitalWrite(foreward3, HIGH);
        digitalWrite(backward3, LOW);
        analogWrite(pwmPin3, pwm3);
      } else {
        digitalWrite(backward3, HIGH);
        digitalWrite(foreward3, LOW);
        analogWrite(pwmPin3, pwm3);
      }
    }
    
    // Print data (if print interval has also elapsed)
    if (currentMillis - printMillis >= printInterval) {
      printMillis = currentMillis;
      
      // Print distances
      Serial.print("Distance 1: ");
      Serial.print(distance1);
      Serial.print(" , PWM: ");
      Serial.println(pwm);

      Serial.print("Distance 2: ");
      Serial.print(distance2);
      Serial.print(" , PWM2: ");
      Serial.println(pwm2);
      
      Serial.print("Distance 3: ");
      Serial.print(distance3);
      Serial.print(" , PWM3: ");
      Serial.println(pwm3);

      Serial.println("");

      Serial.print("Servo: ");
      Serial.println(servoPos);
    }
  }
}
