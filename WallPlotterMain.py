from Position import *


position = Position()
position.set_current_pos(0,0)

position.drive_to(200,0)

for x in range(50,100,10):
    position.drive_to(200,x)
    position.drive_to(200+x,x)
    position.drive_to(200+x,0)
    position.drive_to(200,0)
