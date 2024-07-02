import os
from pathlib import Path
from pprint import pprint

from bytechomp import Reader, ByteOrder, dataclass, Annotated, serialize
from bytechomp.datatypes import U16

ACTION_NUM_BYTE = 6
SERVOS_NUM = 40
SERVO_PREFIX = 21845
ACTIONS_PATH = Path("actions")

# Set path for script.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

rob_filename = "climb.rob"

with open(ACTIONS_PATH / rob_filename, "rb") as f:
    f.seek(ACTION_NUM_BYTE)
    actions_num = int.from_bytes(f.read(1), "big")


@dataclass
class Header:
    prefix: Annotated[bytes, 6]
    params: Annotated[bytes, 10]


@dataclass
class Servo:
    position: U16
    id: U16
    tail: U16


@dataclass
class Action:
    time: U16
    servos: Annotated[list[Servo], SERVOS_NUM + 1]


@dataclass
class RobFile:
    header: Header
    actions: Annotated[list[Action], actions_num]


reader = Reader[RobFile]().allocate()
actions_list = []

with open(ACTIONS_PATH / rob_filename, "rb") as fp:
    while (data := fp.read(4)):
        reader.feed(data)

        if reader.is_complete():
            rob_file = reader.build()
            for action in rob_file.actions: 
                action_dict = {"time": action.time}
                for servo_num, servo in enumerate(action.servos):
                    servo_position = servo.position
                    if (servo_position == SERVO_PREFIX and 
                       servo.id == 0 and 
                       servo.tail == 0): 
                        continue
                    else:
                        action_dict[servo_num] = servo_position
                actions_list += [action_dict]

for action in actions_list:
    print(action)
