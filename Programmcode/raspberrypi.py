from serial_com import Communicator

com = Communicator("COM5")

def main():
    try:
        while True:
            print(*com.wait_for_data(),sep="\n")
            pass
        pass
    finally:
        com.close()
        pass
    pass

if __name__ == "__main__":
    main()
    pass