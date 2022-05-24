# from serial_com import Communicator

# com = Communicator("COM4")

# print(*com.wait_for_data(),sep="\n")

# com.close()

from serial import Serial

con = Serial("COM4")

print(con.readline())

con.close()