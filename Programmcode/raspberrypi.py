from cgitb import reset
from dis import dis
from serial_com import Communicator, Blob
from serial.tools import list_ports_linux
import buildhat
import time
import RPi.GPIO as GPIO

driveline = 0#set correct data
#hardwhare info setup distance sensor to the left

def makeTurn(right: bool, steering):#make the car turn aproxamatly 90 degrees will correct error automaticly probably 
    if right:
        steering.run_to_position(-100, blocking=False) #add correct data to go right
        #wait for run distance on drive (set correct data and code)
    else:
        steering.run_to_position(100, blocking=False) #add correct data to go left 
        #wait for run distance on drive (set correct data and code)



def frame(steering, drive, distance, distance2, imageSize, blobs: list[Blob]):
    
    if(distance < 1000):
        if distance2 > 1000:
            makeTurn(True, steering)
            return
        else:
            makeTurn(False, steering) 
        return
    
    
    redSice = 0
    greenSice = 0
    treshold = 0#set Treshold for minimal sice
    for blob in blobs: 
        if blob.type == "red_pillar":
            redSice += blob.size
        elif blob.type == "green_pillar":
            greenSice += blob.size
    
    if redSice > treshold and redSice>greenSice:
        driveline = 0 #set correct data
    elif greenSice > treshold and greenSice > redSice:
        driveline = 0#set correct data
    
    if distance2 > driveline:
        steering.run_to_position(100, blocking=False) #add correct data to go left 
    elif distance2 < driveline:
        steering.run_to_position(-100, blocking=False) #add correct data to go right 

def main():
    print(*list_ports_linux.comports(),sep="\n")
    cam_port = input("Enter the name for the comport: ")

    GPIO_Port = 5
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_Port, GPIO.IN)

    com = Communicator(cam_port)
    steering_motor = buildhat.Motor("B")
    driving_motor = buildhat.Motor("A")
    distance_sensor = buildhat.DistanceSensor("C")
    color_sensor = buildhat.ColorSensor("D")

    while not GPIO.input(GPIO_Port): 
        time.sleep(1)
        pass
    
    # Set motors to start config
    steering_motor.run_to_position(0)
    driving_motor.start(-25)
    
    try:
        while True:
            im_size, blobs = com.wait_for_data()

            frame(steering_motor, driving_motor, distance_sensor.get_distance(),color_sensor.get_color() , im_size,blobs)
            pass
        pass
    finally:
        com.close()
        driving_motor.stop()
        pass
    pass

if __name__ == "__main__":
    main()
    pass
