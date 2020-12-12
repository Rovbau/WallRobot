from Position import *
from Gcode import *
import atexit
from time import *

def homing():
    print("Goto HOME Position")
    position.drive_to(0,0)

atexit.register(homing)
position = Position()
gcode = Gcode()

position.set_current_pos(0,0)
position.draw_gcode(["G00", 0, 0, None, None, None])
#position.drive_to(200,100)

#position.draw_text("WILKOMMEN-ROBY-UND-FRIENDS", 0.2)

## To Print a picture
##
command_generator = gcode.command_from_file("DinoGross_0001.ngc")

while True:
    try:
        command = command_generator.next()
    except:
        print("File END")
        break
    position.draw_gcode(command)

    print(command)
position.drive_to(0,0)

