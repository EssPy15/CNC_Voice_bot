#include <Servo.h>

// --- Stepper Motor Pins (CNC Shield V3 Standard) ---
#define X_STEP_PIN 2
#define Y_STEP_PIN 3
#define X_DIR_PIN  5
#define Y_DIR_PIN  6
#define EN_PIN     8  // Active LOW to enable stepper drivers

// --- Servo Pin (Your Bypass Pin) ---
#define SERVO_PIN  11 
Servo penServo;

void setup() {
  // 1. Configure stepper pins
  pinMode(X_STEP_PIN, OUTPUT);
  pinMode(Y_STEP_PIN, OUTPUT);
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(Y_DIR_PIN, OUTPUT);
  pinMode(EN_PIN, OUTPUT);

  // 2. Enable Stepper Drivers (LOW turns them ON)
  digitalWrite(EN_PIN, LOW);

  // 3. Initialize Servo
  penServo.attach(SERVO_PIN);
  penServo.write(90); // Start with pen UP
  delay(1000);
}

void loop() {
  // --- SEQUENCE 1: Drop Pen and Move Forward ---
  
  // 1. Drop the pen (Servo down)
  penServo.write(0); 
  delay(500); // Wait for servo to physically move

  // 2. Set direction to FORWARD
  digitalWrite(X_DIR_PIN, HIGH);
  digitalWrite(Y_DIR_PIN, HIGH);

  // 3. Step the X and Y motors (400 steps = 2 full revolutions usually)
  for (int i = 0; i < 400; i++) {
    digitalWrite(X_STEP_PIN, HIGH);
    digitalWrite(Y_STEP_PIN, HIGH);
    delayMicroseconds(1000); // Speed: Lower number = faster, Higher = slower
    digitalWrite(X_STEP_PIN, LOW);
    digitalWrite(Y_STEP_PIN, LOW);
    delayMicroseconds(1000);
  }
  
  delay(500); // Pause at the end of the line


  // --- SEQUENCE 2: Lift Pen and Return to Start ---

  // 1. Lift the pen (Servo up)
  penServo.write(90);
  delay(500);

  // 2. Set direction to BACKWARD
  digitalWrite(X_DIR_PIN, LOW);
  digitalWrite(Y_DIR_PIN, LOW);

  // 3. Step motors back to the starting point
  for (int i = 0; i < 400; i++) {
    digitalWrite(X_STEP_PIN, HIGH);
    digitalWrite(Y_STEP_PIN, HIGH);
    delayMicroseconds(1000); 
    digitalWrite(X_STEP_PIN, LOW);
    digitalWrite(Y_STEP_PIN, LOW);
    delayMicroseconds(1000);
  }

  // Wait 2 seconds before doing it all again
  delay(2000);
}