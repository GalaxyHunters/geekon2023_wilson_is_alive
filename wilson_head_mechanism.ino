#include <Servo.h>
#define BUTTON_PIN 5
#define SERVO_PIN 9

// Set Vars
Servo head_ctrl; 
int pos = 0;
byte lastButtonState = LOW;

void setup() {
  Serial.begin(9600);
  head_ctrl.attach(SERVO_PIN); 
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  byte buttonState = digitalRead(BUTTON_PIN);

  if (buttonState != lastButtonState) { // Check if push-button was pressed
    lastButtonState = buttonState;
    if (buttonState == LOW) { // Rotate the head servo back-and-forth for a random period of time
      for (pos = 0; pos <= 180; pos += 1) { 
        head_ctrl.write(pos);              
        delay(random(20,40));                       
      }
      for (pos = 180; pos >= 0; pos -= 1) { 
        head_ctrl.write(pos);              
        delay(random(20,40));                       
      }
    }
  }
}
