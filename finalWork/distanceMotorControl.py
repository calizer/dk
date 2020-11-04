#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
#set Ultrasonic GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 22
maxTime = 0.04

#set motor GPIO Pins
in1 = 14
in2 = 15
en = 12
temp1=1

#motor setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,50)
p.start(75)

prevDist = 0
currDist = 0

def distance():
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.01)
    
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
        
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    timeout = StartTime + maxTime
    
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0 and StartTime < timeout:
        StartTime = time.time()
 
    StopTime = time.time()
    timeout = StopTime + maxTime
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1 and StopTime < timeout:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 17500)
    distance = round(distance, 2)
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            currDist = distance()
            if(currDist < 1.0):
                currDist = prevDist
                #print ("Measured Distance = %.1f cm" % currDist)
            else:
                prevDist = currDist
                #print ("Measured Distance = %.1f cm" % currDist)
            
            if(currDist > 40.0):
                p.ChangeDutyCycle(80)
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                print ("FAR! Measured Distance = %.1f cm" % currDist)
            elif(currDist < 40.0 and currDist > 20.0):
                p.ChangeDutyCycle(50)
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                print ("CLOSE! Measured Distance = %.1f cm" % currDist)
            else:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                print ("STOPPED! Measured Distance = %.1f cm" % currDist)
                
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
