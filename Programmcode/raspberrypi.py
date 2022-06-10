from serial_com import Communicator, Blob
from serial.tools import list_ports_linux
import buildhat
import time
import RPi.GPIO as GPIO

driveline = 500#set correct data
#hardwhare info setup distance sensor to the left

def maxRangeConvert(distance: int):
    if distance == -1:
        return 15000
    else:
        return distance
    pass

TURN_TIME = 1.2
LAST_TURN_TIME = -TURN_TIME
def makeTurn(right: bool, steering, drive):#make the car turn aproxamatly 90 degrees will correct error automaticly probably 
    global LAST_TURN_TIME
    current_time = time.perf_counter()
    # print("Time: ",current_time - LAST_TURN_TIME)
    if current_time - LAST_TURN_TIME <= TURN_TIME: return
    LAST_TURN_TIME = current_time
    
    if right:
        steering.run_to_position(MAIN_TURN, blocking=False) #add correct data to go right
    else:
        steering.run_to_position(-MAIN_TURN, blocking=False) #add correct data to go left 


TURN_DISTANCE = 1_000
MAIN_TURN = 100
SIDE_ADJUST_ANGLE = 20
def frame(steering, drive, distance, distance2, imageSize, blobs: list[Blob]):
    global driveline
    
    print("Head distance:",distance)
    print("Side adjust enabled:", time.perf_counter()-LAST_TURN_TIME > TURN_TIME)
    
    if(distance < TURN_DISTANCE):
        if distance2 > 1200:
            makeTurn(True, steering, drive)
            #driveline = 900
            return
        else:
            makeTurn(False, steering, drive) 
            #driveline = 100
            return
    
    
    redSize = 0
    greenSize = 0
    treshold = 100#set Treshold for minimal size
    for blob in blobs: 
        if blob.type == "red_pillar":
            redSize += blob.area
        elif blob.type == "green_pillar":
            greenSize += blob.area
    
    # if redSize > treshold and redSize>greenSize:
    #     driveline = 900 #set correct data
    # elif greenSize > treshold and greenSize > redSize:
    #     driveline = 50#set correct data
    if time.perf_counter()-LAST_TURN_TIME > TURN_TIME and distance2 <= 1200: # correct sidebarier distance catch
        #print(distance2)
        if distance2 > driveline: # correct exeptet error range 
            #print("Left")
            steering.run_to_position(SIDE_ADJUST_ANGLE, blocking=False) #add correct data to go left 
        elif distance2 < driveline:#correct exepted error 
            #print("Right")
            steering.run_to_position(-SIDE_ADJUST_ANGLE, blocking=False) #add correct data to go right 
        else:
            #print("None")
            steering.run_to_position(0, blocking=False)#make vehicel go streight 

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
    distance_sensor_2 = buildhat.DistanceSensor("D")

    while not GPIO.input(GPIO_Port): 
        time.sleep(1)
        pass
    
    # Set motors to start config
    steering_motor.run_to_position(0)
    driving_motor.start(-100)
    
    try:
        while True:
            im_size, blobs = com.wait_for_data()

            #print("Distance:",distance_sensor.get_distance())
            frame(
                steering_motor, 
                driving_motor, 
                maxRangeConvert(distance_sensor.get_distance()), 
                maxRangeConvert(distance_sensor_2.get_distance()) , 
                im_size,blobs
            )
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
