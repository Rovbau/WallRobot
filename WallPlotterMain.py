from Position import *
from Gcode import *
from math import sin, cos, radians
import atexit

def homing():
    print("HOME Pos.")
    position.drive_to(0,0)
 

atexit.register(homing)
position = Position()
gcode = Gcode()

position.set_current_pos(0,0)

command_generator = gcode.command_from_file("DinoGross_0001.ngc")

while True:
    try:
        command = command_generator.next()
    except:
        print("File END")
        break
    print(command)
    if command[0] == "G00":
        if command[1] != None and command[2] != None:
            position.drive_to(x = float(command[1]), y = float(command[2]))
    if command[0] == "G01":
        if command[1] != None and command[2] != None:
            position.drive_to(x = float(command[1]), y = float(command[2]))
            position.drive_to(x = command[1], y = command[2])
    if command[0] == "G02" or command[0] == "G03":
        position.draw_circle(g_code = command[0], x = command[1], y = command[2], i = command[4], j = command[5])


#position.drive_to(80,120)
#position.draw_text("IRIS-HELMING", 0.1)
#position.drive_to(0,0)



##position.drive_to(100,100)
##position.draw_circle(62,100,-20,0)
##position.drive_to(0,0)

#position.drive_to(50,50)
#for i in range(0,180,1):
 #   #print(sin(radians(90)))
  #  zoom = 40
   # i = radians(i)
   # position.drive_to(100+zoom*sin(i),100+zoom*cos(i))
