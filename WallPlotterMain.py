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
##
##position.set_current_pos(0,0)
##position.drive_to(300,0)
##position.drive_to(300,200)
position.drive_to(0, 300)
##position.drive_to(200,0)
sleep(4)
#position.draw_text("EIN-GRUSS-VON-ROBI", 0.2)

##command_generator = gcode.command_from_file("DinoGross_0001.ngc")
##
##start_time = time()
##
##while True:
##    try:
##        command = command_generator.next()
##    except:
##        print("File END")
##        break
##    position.draw_gcode(command)
##    
##    print(command)

#print("Draw for %.4g Sec") % (time() - start_time)

#position.drive_to(80,120)
#position.draw_text("IRIS-HELMING", 0.1)
#position.drive_to(0,0)

