#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

const float FALL_THRESHOLD = 2.5; // in g units (adjust as needed)
unsigned long lastFallAlertTime = 0;
const unsigned long FALL_ALERT_COOLDOWN = 5000; // milliseconds

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();

  if (mpu.testConnection()) {
    Serial.println("MPU6050 connected.");
  } else {
    Serial.println("MPU6050 connection failed.");
  }
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  // Convert raw values to g's (assuming +/-2g full scale)
  float AccX = ax / 16384.0;
  float AccY = ay / 16384.0;
  float AccZ = az / 16384.0;

  float AccMagnitude = sqrt(AccX * AccX + AccY * AccY + AccZ * AccZ);

  Serial.print("Acceleration magnitude (g): ");
  Serial.println(AccMagnitude);

  unsigned long currentMillis = millis();

  // Detect falls - spike above threshold or free fall (less than 0.5g)
  if ((AccMagnitude > FALL_THRESHOLD || AccMagnitude < 0.5) &&
      (currentMillis - lastFallAlertTime > FALL_ALERT_COOLDOWN)) {
    Serial.println("FALL DETECTED! Activate alert!");
    // TODO: Activate vibration or alert signal here
    lastFallAlertTime = currentMillis;
  }

  delay(200); // adjust sample rate as needed
}
