import serial, json, dataclasses

@dataclasses.dataclass(frozen=True)
class Blob:
    type: str
    left_top: list[int,int]
    size: list[int,int]

    @property
    def left(self) -> int:
        return self.left_top[0]
        pass

    @property
    def right(self) -> int:
        return self.left_top[0] + self.size[0]
        pass

    @property
    def top(self) -> int:
        return self.left_top[1]
        pass

    @property
    def bottom(self) -> int:
        return self.left_top[1] + self.size[1]
        pass

    @property
    def width(self) -> int:
        return self.size[0]
        pass

    @property
    def height(self) -> int:
        return self.size[1]
        pass

    @property
    def center_x(self) -> int:
        return self.left + self.width/2
        pass

    @property
    def center_y(self) -> int:
        return self.top + self.height/2
        pass

    @property
    def center(self) -> tuple[int,int]:
        return self.center_x, self.center_y
        pass
    pass

class Communicator:
    __slots__ = "conn",
    def __init__(self, port : str, *, baudrate : int = 115200):
        self.conn = serial.Serial(port,baudrate)
        pass

    def _read_packet(self) -> str:
        return self.conn.readline()
        pass

    
    def wait_for_data(self) -> list[Blob]:
        while self._read_packet() != "BEGIN": # Wait for beginning of data transfer
            pass
        
        new_blobs = []
        while True:
            last_data = self._read_packet()
            if last_data == "END": 
                break

            new_blobs.append(Blob(**json.loads(last_data)))
            pass

        return new_blobs
        pass

    def close(self):
        self.conn.close()
        pass
    pass