#include <DistanceSensor.h>
#include <AFMotor.h>
#include <string.h>
// Define pins
const int echoPin1 = 33;
const int trigPin1 = 31;
const int echoPin2 = 44;
const int trigPin2 = 42;
const int buzzerPin = 26;

// Start the sensor
DistanceSensor sensor1(trigPin1, echoPin1);
DistanceSensor sensor2(trigPin2, echoPin2);
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);// The motor number, i.e. 1, 2, 3 or 4
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

void setup() {
  //TODO
    Serial3.begin(9600);
    //Serial3.begin(9600);
    pinMode(buzzerPin,OUTPUT);//端口定义
    loud();
    motor1.setSpeed( 100 );
    motor2.setSpeed( 100 );
    motor3.setSpeed( 100 );
    motor4.setSpeed( 100 );
    
    motor2.run(RELEASE);
    motor3.run(RELEASE);
    motor1.run(RELEASE);
    motor4.run(RELEASE);
}

void FASTforward()
{
    motor1.setSpeed( 255 );
    motor2.setSpeed( 255 );
    motor3.setSpeed( 255 );
    motor4.setSpeed( 255 );
    motor2.run(BACKWARD);
    motor3.run(FORWARD);
    motor1.run(FORWARD);
    motor4.run(BACKWARD);
    delay(500);  
}

void FASTbackward()
{
    motor1.setSpeed( 255 );
    motor2.setSpeed( 255 );
    motor3.setSpeed( 255 );
    motor4.setSpeed( 255 );  
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
    motor2.run(BACKWARD);
    motor3.run(FORWARD);
    motor1.run(FORWARD);
    motor4.run(BACKWARD);
    delay(500);  
}

void backward()
{
    motor1.setSpeed( 150 );
    motor2.setSpeed( 150 );
    motor3.setSpeed( 150 );
    motor4.setSpeed( 150 );  
    motor2.run(FORWARD);
    motor3.run(BACKWARD);
    motor1.run(BACKWARD);
    motor4.run(FORWARD);
    delay(500);
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
    delay(250);
    motor2.run(RELEASE);
    motor3.run(RELEASE);
    motor1.run(RELEASE);
    motor4.run(RELEASE);
    
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
    delay(250);
    motor2.run(RELEASE);
    motor3.run(RELEASE);
    motor1.run(RELEASE);
    motor4.run(RELEASE);
}

void still()
{
   motor2.run(RELEASE);
   motor3.run(RELEASE);
   motor1.run(RELEASE);
   motor4.run(RELEASE);
   delay(500);
}

void loud()
{
    for(int i=600;i<=750;i++)//频率不断上升
    {
      tone(buzzerPin,230);
      delay(5);
    }
    noTone(buzzerPin);
}

int dis1;
int dis2;

void loop() {
    dis1=sensor1.getCM();
    dis2=sensor2.getCM();
    //+Serial.print(dis);
    if(dis1<=50||dis2<=50)
    {
      still();
      delay(100);
      loud();
      delay(100);
    }
    if (Serial3.available()) {
      //TODO
        char input = Serial3.read();
        if (input == '+')
          FASTforward();
        else if (input == '-')
          FASTbackward();
        else if (input=='w')
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
    
    }
  
}
