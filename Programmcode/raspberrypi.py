from serial_com import Communicator, Blob
from serial.tools import list_ports_linux
import buildhat
import time
import RPi.GPIO as GPIO

def frame(steering_motor, driving_motor, distance, im_size, blobs : list[Blob]):
    
    pass

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

    while not GPIO.input(GPIO_Port): 
        time.sleep(1)
        pass

    driving_motor.start(100)
    try:
        while True:
            im_size, blobs = com.wait_for_data()

            frame(steering_motor, driving_motor, distance_sensor.get_distance(), im_size,blobs)
            pass
        pass
    finally:
        com.close()
        pass
    pass

if __name__ == "__main__":
    main()
    pass