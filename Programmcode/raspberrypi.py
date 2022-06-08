from serial_com import Communicator, Blob
from serial.tools import list_ports_linux
import buildhat
import time
import RPi.GPIO as GPIO

def frame(steering, drive, distance, color, imageSize, blobs: list[Blob]):
    if(distance < 1000):
        if color == "Orange" : #add real values
            steering.run_to_position(100, False) #correct values
        elif color == "blue": #add real values
            steering.run_to_position(-100,False) #correct values
    
    """if no wall blobs infront of camara stop turning""" #possably timing the turn 
    for blob in blobs:
        if blob.type == "wall":
            if blob.bottom <= imageSize[1] - 20: #add correct value
                if blob.center_x < imageSize[0] // 2:
                    steering.run_to_position(100,False) #add correct data
                elif blob.center_x > imageSize[0] // 2:
                    steering.run_to_position(-100,False) #add correct data
    

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

    driving_motor.start(100)
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