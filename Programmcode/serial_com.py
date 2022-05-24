import serial, json, dataclasses, time

@dataclasses.dataclass(frozen=True)
class Blob:
    type: str
    left_top: list[int,int]
    size: list[int,int]

    @staticmethod
    def from_json(data : dict):
        return Blob(
            data["type"],
            data["left_top"],
            data["size"]
        )
        pass

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
        while not self.conn.readline().startswith(b"BEGIN"): time.sleep(0.1)
    
        end_encountered = False
        lines = []
        while not end_encountered:
            data = self.conn.readline().decode("utf-8")

            if data.startswith("END"):
                end_encountered = True
                pass
            else:
                lines.append(data)
                pass
            pass

        json_decoded = [json.loads(line) for line in lines]

        return [Blob.from_json(data) for data in json_decoded]
        pass

    def close(self):
        self.conn.close()
        pass
    pass