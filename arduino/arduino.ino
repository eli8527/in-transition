int fAForward = 1;
int fABackward = 2;
int fAPower = 3;

int fBForward = 4;
int fBBackward = 5;
int fBPower = 6;

int bAForward = 7;
int bABackward = 8;
int bAPower = 9;

int bBForward = 12;
int bBBackward = 11;
int bBPower = 10;

int fPressure = A3;
int fIR = A0;
int bPressure = A2;
int bIR = A1;

const int STOP = 0;
const int FORWARD = 1;
const int BACKWARD = 2;
const int SIDEWAYSL = 3;
const int SIDEWAYSR = 4;

int directionState = 0; // [0,4]
int power = 0; // [0, 255]

void setup() {

  // Iterates through all motor related pins and sets to output
  for (int i = 1; i <= 12; i++) {
    pinMode(i, OUTPUT);
  }

  Serial.begin(9600);

}

void loop() {
  // Print Readings
  int fPressureValue = analogRead(fPressure); // CALIBRATE
  int bPressureValue = analogRead(bPressure); // CALIBRATE

//  Serial.print(fPressureValue);
//  Serial.print(",");
//  Serial.println(bPressureValue);

  // Handle movement
  while(Serial.available() > 0) {
      // State
      
      // Either
      // 0 = Stopped
      // 1 = Forward
      // 2 = Backward
      // 3 = Sideways Left
      // 4 = Sideways right
      directionState = Serial.parseInt();
      directionState = constrain(directionState, 0, 4);
      
      power = Serial.parseInt();
      power = constrain(power, 0, 255);
  }

  if (directionState == FORWARD) {
    moveForward(power);
  } else if (directionState == BACKWARD) {
    moveBackward(power);
  } else if (directionState == SIDEWAYSL) {
    moveSidewaysLeft(power);
  } else if (directionState == SIDEWAYSR) {
    moveSidewaysRight(power);
  } else {
    // CASE == STOP OR SOME ARBITRARY STATE
    stopMovement();
    // just in case
    power = 0;
  }

  Serial.print(directionState);
  Serial.print(",");
  Serial.println(power);

}

// Sets powers to 0
void stopMovement() {
  analogWrite(fAPower, 0);
  analogWrite(fBPower, 0);
  analogWrite(bAPower, 0);
  analogWrite(bBPower, 0);
}

// Power 0 to 255
void moveForward(int power) {
  digitalWrite(fAForward, HIGH);
  digitalWrite(fABackward, LOW);
  analogWrite(fAPower, power);

  digitalWrite(fBForward, HIGH);
  digitalWrite(fBBackward, LOW);
  analogWrite(fBPower, power);

  digitalWrite(bAForward, HIGH);
  digitalWrite(bABackward, LOW);
  analogWrite(bAPower, power);

  digitalWrite(bBForward, HIGH);
  digitalWrite(bBBackward, LOW);
  analogWrite(bBPower, power);
}

// Power 0 to 255
void moveBackward(int power) {
  digitalWrite(fAForward, LOW);
  digitalWrite(fABackward, HIGH);
  analogWrite(fAPower, power);

  digitalWrite(fBForward, LOW);
  digitalWrite(fBBackward, HIGH);
  analogWrite(fBPower, power);

  digitalWrite(bAForward, LOW);
  digitalWrite(bABackward, HIGH);
  analogWrite(bAPower, power);

  digitalWrite(bBForward, LOW);
  digitalWrite(bBBackward, HIGH);
  analogWrite(bBPower, power);
}

// Power 0 to 255
void moveSidewaysLeft(int power) {
  digitalWrite(fAForward, LOW);
  digitalWrite(fABackward, HIGH);
  analogWrite(fAPower, power);

  digitalWrite(fBForward, LOW);
  digitalWrite(fBBackward, HIGH);
  analogWrite(fBPower, power);

  digitalWrite(bAForward, HIGH);
  digitalWrite(bABackward, LOW);
  analogWrite(bAPower, power);

  digitalWrite(bBForward, HIGH);
  digitalWrite(bBBackward, LOW);
  analogWrite(bBPower, power);
}

// Power 0 to 255
void moveSidewaysRight(int power) {
  digitalWrite(fAForward, HIGH);
  digitalWrite(fABackward, LOW);
  analogWrite(fAPower, power);

  digitalWrite(fBForward, HIGH);
  digitalWrite(fBBackward, LOW);
  analogWrite(fBPower, power);

  digitalWrite(bAForward, LOW);
  digitalWrite(bABackward, HIGH);
  analogWrite(bAPower, power);

  digitalWrite(bBForward, LOW);
  digitalWrite(bBBackward, HIGH);
  analogWrite(bBPower, power);
}
