#
# Class helper to calculate Position for Wall Drawing Robot with Stepper Motor

from math import *

class Stepper():
    def __init__(self, counts_per_mm):
        self. counts_per_mm = counts_per_mm
        self.old = 0
    
    def goto_pos(self, lenght):
        print("DRIVE TO: " +str(lenght))
        
        
class Position():
    def __init__(self):
        self.stepper1 = Stepper(1)
        self.stepper2 = Stepper(1)
        
        self.motor_dist = 100
        self.canvas_high = 100

    def set_current_pos(self, x, y):
        self.current_x = x
        self.current_y = y
        
       
    def bresenham(self, x0, y0, x1, y1):
        """Yield integer coordinates on the line from (x0, y0) to (x1, y1).
        Input coordinates [mm], internaly roundet to 1/10mm"""

        x0 = int(x0*10)
        y0 = int(y0*10)
        x1 = int(x1*10)
        y1 = int(y1*10)
        
        dx = x1 - x0
        dy = y1 - y0

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2*dy - dx
        y = 0

        for x in range(dx + 1):
            yield float(x0 + x*xx + y*yx)/10, float(y0 + x*xy + y*yy)/10
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy
            
    def drive_to(self, x, y):
        """drives the gondola to the position x,y [mm]"""      
        line_generator = self.bresenham(self.current_x, self.current_y, x, y)

        while True:
            try:
                path_x, path_y = line_generator.next()
            except StopIteration:
                break
            print(path_x, path_y)    
            wire1, wire2 = self.get_wire_lenght(path_x, path_y)            
            self.stepper1.goto_pos(wire1)
            self.stepper2.goto_pos(wire2)

        print()
            
    def get_wire_lenght(self,x, y):
        """calc the wire lenght for two motors, pythagoras
        Returns: INT lenght M1, M2 [mm]"""
        x_motor1 = x
        x_motor2 = self.motor_dist - x
        y_motor  = self.canvas_high - y
        wire1 = sqrt(pow(x_motor1,2) + pow(y_motor,2))
        wire2 = sqrt(pow(x_motor2,2) + pow(y_motor,2))
        
        return(round(wire1,2), round(wire2,2))


if __name__ == "__main__":


    position = Position()
    position.set_current_pos(10,40)
    position.drive_to(10,41)


        
    
