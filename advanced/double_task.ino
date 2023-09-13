#include <DistanceSensor.h>
#include <AFMotor.h>
#include <string.h>
#include <Servo.h>
#include <SCoop.h>
// Define pins
const int echoPin1 = 33;
const int trigPin1 = 31;
const int echoPin2 = 44;
const int trigPin2 = 42;
const int buzzerPin = 26;
const int LED_avoid = 43;
const int button = 45;

// Start the sensor
DistanceSensor sensor1(trigPin1, echoPin1);
DistanceSensor sensor2(trigPin2, echoPin2);
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);// The motor number, i.e. 1, 2, 3 or 4
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
Servo servo1;


void setup() {
    mySCoop.start();
    Serial.begin(9600);
    Serial3.begin(9600);
    
}

void FASTforward()
{
    motor1.setSpeed( 300 );
    motor2.setSpeed( 300 );
    motor3.setSpeed( 300 );
    motor4.setSpeed( 300 );
    motor2.run(BACKWARD);
    motor3.run(FORWARD);
    motor1.run(FORWARD);
    motor4.run(BACKWARD);
    delay(500);  
}

void FASTbackward()
{
    motor1.setSpeed( 300 );
    motor2.setSpeed( 300 );
    motor3.setSpeed( 300 );
    motor4.setSpeed( 300 );  
    motor2.run(FORWARD);
    motor3.run(BACKWARD);
    motor1.run(BACKWARD);
    motor4.run(FORWARD);
    delay(500);
}

void forward()
{
    motor1.setSpeed( 150 );
    motor2.setSpeed( 150 );
    motor3.setSpeed( 150 );
    motor4.setSpeed( 150 );  
    motor2.run(FORWARD);
    motor3.run(BACKWARD);
    motor1.run(BACKWARD);
    motor4.run(FORWARD);
    delay(200); 
}

void backward()
{
    motor1.setSpeed( 150 );
    motor2.setSpeed( 150 );
    motor3.setSpeed( 150 );
    motor4.setSpeed( 150 );
    motor2.run(BACKWARD);
    motor3.run(FORWARD);
    motor1.run(FORWARD);
    motor4.run(BACKWARD);
    delay(200);  
    
}

void right()
{
    motor2.setSpeed(250);
    motor3.setSpeed(250);
    motor1.setSpeed(250);
    motor4.setSpeed(250);
    motor2.run(BACKWARD);
    motor3.run(BACKWARD);
    motor1.run(FORWARD);
    motor4.run(FORWARD);
    delay(1000);
    
    
}

void left()
{
    motor2.setSpeed(250);
    motor3.setSpeed(250);
    motor1.setSpeed(250);
    motor4.setSpeed(250);
    motor2.run(FORWARD);
    motor3.run(FORWARD);
    motor1.run(BACKWARD);
    motor4.run(BACKWARD);
    delay(1000);
   
    
    
}

void loud()
{ 
    tone(buzzerPin,300);
    delay(500);
    noTone(buzzerPin);
}

void still()
{
   motor2.run(RELEASE);
   motor3.run(RELEASE);
   motor1.run(RELEASE);
   motor4.run(RELEASE);
   delay(200);
}



int dis1;
int dis2;
int angle=90;
int val;

defineTask(movement)

void movement::setup()
{
  pinMode(buzzerPin,OUTPUT);//端口定义
    pinMode(LED_avoid,OUTPUT);
    pinMode(button,INPUT);
    loud();
    servo1.attach(39);
    motor1.setSpeed( 100 );
    motor2.setSpeed( 100 );
    motor3.setSpeed( 100 );
    motor4.setSpeed( 100 );
    
    motor2.run(RELEASE);
    motor3.run(RELEASE);
    motor1.run(RELEASE);
    motor4.run(RELEASE);
}

void movement::loop()
{
  if (Serial3.available()) 
  {
      //TODO
        char input = Serial3.read();
        val=digitalRead(button);
    if(val == 0)
    {
      still();
      digitalWrite(LED_avoid,LOW);
      //loud();
      delay(10);
    }
    else
    {
      digitalWrite(LED_avoid,HIGH);
      delay(10);
    }
    dis1=sensor1.getCM();
    //dis2=sensor2.getCM();
    //Serial3.print(dis);
    //TODO
    if(dis1<=40)
    {
      still();
      delay(5);
      loud();
      delay(5);
      
    }
        if (input=='w')
        {
          forward();
        }
        else if(input=='s')
        {
          backward();
        }
        else if(input=='a')
        {
          left();
        }
        else if(input=='d')
        {
          right();
        }
        else if(input=='g')
        {
          still();
        }
        else if(input=='l')
        {
          loud();
          delay(200);
        }
}
}



defineTaskLoop(follower)
{
  if (Serial3.available()) {
        char input = Serial3.read();
        if(input=='e' && angle>15)
        {
          if(angle<=10)
          {
            return;
          }
          angle-=10;
          servo1.write(angle); 
        }
        else if(input=='q' && angle<165)
        {
          if(angle>=170)
          {
            return;
          }
          angle+=10;
          servo1.write(angle);
        }
        
    }
}

void loop() {
   yield();
    
  
}
