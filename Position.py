#
# Class helper to calculate Position for Wall Drawing Robot with Stepper Motor

from math import *
from Stepper import *
from Lifter import *
from colorama import Fore, Style
        
class Position():
    def __init__(self):

        self.motor_dist = 816
        self.canvas_high = 500

        mm_per_step = 0.08
        
        length1, length2 = self.get_wire_lenght(0,0)
        home_counts1 = length1 / mm_per_step
        home_counts2 = length2 / mm_per_step
       
        self.stepper1 = Stepper("Left",  mm_per_step = 0.08,
                        pin_dir = 35, pin_step = 37, actual = home_counts1)
        self.stepper2 = Stepper("Right", mm_per_step = 0.08,
                        pin_dir = 31, pin_step = 33, actual = home_counts2)
        self.lifter = Lifter(PIN = 29)
        
        self.current_x = 0
        self.current_y = 0

    def set_current_pos(self, x, y):
        """Set program state to position x,y"""
        self.current_x = x
        self.current_y = y
        
    def get_current_pos(self):
        """Get the current gondola position"""
        return(self.current_x, self.current_y)
       
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
        """Drives the gondola to the position x,y [mm]"""      
        line_generator = self.bresenham(self.current_x, self.current_y, x, y)

        #print("Drive to: " + str(round(x,2)) + " "+ str(round(y,2)))
        
        while True:
            try:
                path_x, path_y = line_generator.next()
            except StopIteration:
                break          
            wire1, wire2 = self.get_wire_lenght(path_x, path_y)
            self.stepper1.goto_pos(wire1)
            self.stepper2.goto_pos(wire2)
        self.set_current_pos(x,y)
            
    def get_wire_lenght(self,x, y):
        """calc the wire lenght for two motors, pythagoras
        Returns: INT lenght M1, M2 [mm]"""
        x_motor1 = x
        x_motor2 = self.motor_dist - x
        y_motor  = self.canvas_high - y
        wire1 = sqrt(pow(x_motor1,2) + pow(y_motor,2))
        wire2 = sqrt(pow(x_motor2,2) + pow(y_motor,2))  
        return(round(wire1,2), round(wire2,2))


    def draw_text(self, text, zoom):
        """Draw a very rude text font. Input: STR Text, INT zoomfactor"""
        SPACING = 35 * zoom
        local_x, local_y = self.get_current_pos()

        for letter in text.upper():
            print(letter)
            self.drive_to(local_x + SPACING, local_y)
            local_x, local_y = self.get_current_pos()

            if letter in font: 
                lines = font[letter]
            else:
                lines = font["-"]
            for line in lines:
                self.drive_to(local_x + line[1]* zoom, local_y + line[2]* zoom)

    def draw_circle(self, g_code, x, y, i, j):
        """Draw a circel from g_code command G02= CW, G03=CCW
        Exapl: G03, endpos_x, endpos_y, deltaR_x_toCurrentPos, deltaR_y_toCurrentPos"""
        
        if g_code == "G03":
            rotation = 361
            rotation_step = 1
        elif g_code == "G02":
            rotation = -361
            rotation_step = -1
        else:
            print("Error parsing Code G02/G03")
            
        actual_x, actual_y = self.get_current_pos()

        #Global center pos.
        center_x = actual_x + i
        center_y = actual_y + j
        #print(center_x, center_y)

        #shift center to 0,0
        reduced_x = actual_x - center_x 
        reduced_y = actual_y - center_y
        #print(reduced_x, reduced_y)

        #Tolerance at the end of circel command. radii bigger->higher tolerance
        tolerance = 0.2 + (max(abs(reduced_x), abs(reduced_y)) / 1000)
        #Rotation step depends on radii. radii bigger->smaller steps
        rotation_step = rotation_step * (0.1 + (1  / (max(abs(reduced_x), abs(reduced_y))/10)))
     
        for arc in range(0,rotation*10,int(rotation_step*10)):
            angle = radians(float(arc)/10)

            actual_x, actual_y = self.get_current_pos()
            if abs(actual_x - x) < tolerance and abs(actual_y - y) < tolerance:
                break
            #print("Diff X: "+str(abs(actual_x - x)))
            #print("Diff Y: "+str(abs(actual_y - y)))

            #Rotationmatrix
            rotate_x = reduced_x * cos(angle) - reduced_y * sin(angle)
            rotate_y = reduced_x * sin(angle) + reduced_y * cos(angle)
            #print(rotate_x, rotate_y)

            drive_x = center_x + rotate_x
            drive_y = center_y + rotate_y
            self.drive_to(drive_x,drive_y)
            #print(drive_x, drive_y)
            
        self.drive_to(x,y)

        #G3 start/end pos. does not meet tolerance
        if abs(actual_x - x) > 0.5 or abs(actual_y - y) > 0.5:
            print(Fore.RED + "Circel Command FAILED Diff: "
                  + str(round(actual_x - x, 3)) + " "
                  + str(round(actual_y - y, 3))
                  + Style.RESET_ALL)

    def draw_gcode(self, command):
        """Draw the G_code command
        G00 = fast_no_drawing; G01 = draw
        G02 = CW circel; G03 = CCW circel
        Input: LIST [g_code, x, y, i, y]"""
        
        if command[0] == "G00":
            if command[1] != None and command[2] != None:
                self.lifter.goto("up")
                self.drive_to(x = float(command[1]), y = float(command[2]))

        if command[0] == "G01":
            if command[1] != None and command[2] != None:
                self.lifter.goto("down")
                self.drive_to(x = float(command[1]), y = float(command[2]))
                self.drive_to(x = command[1], y = command[2])
                
        if command[0] == "G02" or command[0] == "G03":
            self.lifter.goto("down")
            self.draw_circle(g_code = command[0], x = command[1], y = command[2], i = command[4], j = command[5])
                
font ={
"A":[["G1",10,27],["G1",20,0],["G0",5,10],["G1",15,10]],
"B":[["G1",0 ,27],["G1",15,27],["G1",18,20],["G1",10,14],["G1",18,7 ],["G1",15,0 ],["G1",0 ,0 ]],
"C":[["G0",20,10],["G1",10,0 ],["G1",0 ,13],["G1",10,27],["G1",20,20]],
"D":[["G1",0 ,27],["G1",10,27],["G1",20,13],["G1",10,0 ],["G1",0 ,0 ]],
"E":[["G1",0 ,27],["G1",20,27],["G0",0 ,13],["G1",20 ,13],["G0",0 ,0 ],["G1",0 ,20]],
"F":[["G1",0 ,27],["G1",18,27],["G0",0 ,13],["G1",15,13]],
"G":[["G0",11,13],["G1",23,13],["G1",23,0 ],["G1",0 ,0 ],["G1",0 ,27],["G1",23,27]],
"H":[["G1",0 ,27],["G0",20,0 ],["G1",20,27],["G0",0 ,13],["G1",20,13]],
"I":[["G1",0 ,27]],
"J":[["G0",0 ,10],["G1",7 ,0 ],["G1",14,10],["G1",14,27]],
"K":[["G1",0 ,27],["G1",20,27],["G1",0 ,13],["G1",20,0 ]],
"L":[["G0",0 ,27],["G1",0 ,0 ],["G1",15 ,0]],
"M":[["G1",0 ,27],["G1",12,0 ],["G1",24,27],["G1",24,0 ]],
"N":[["G1",0 ,27],["G1",18,0 ],["G1",18,27]],
"O":[["G0",0 ,13],["G1",12,27],["G1",24,13],["G1",12,0 ],["G1",0 ,13]],
"P":[["G1",0 ,27],["G1",12,27],["G1",18,20],["G1",12,13],["G1",0 ,13]],
"Q":[["G0",0 ,13],["G1",12,27],["G1",24,13],["G1",12,0 ],["G1",0 ,13],["G0",15,10],["G1",24,0 ]],
"R":[["G1",0 ,27],["G1",12,27],["G1",18,20],["G1",12,13],["G1",0 ,13],["G1",20,0]],
"S":[["G0",0 ,10],["G1",9 ,0 ],["G1",18,13],["G1",0 ,22],["G1",9 ,27],["G1",18,22]],
"T":[["G0",11,0 ],["G1",11,27],["G0",0 ,27],["G1",22,27]],
"U":[["G0",0 ,27],["G1",0 ,0 ],["G1",20,0 ],["G1",20,27]],
"V":[["G0",0 ,27],["G1",10,0 ],["G1",20,29]],
"W":[["G0",0 ,27],["G1",8 ,0 ],["G1",16,27],["G1",24,0 ],["G1",32,27]],
"X":[["G1",20,27],["G0",0 ,27],["G1",20,0 ]],
"Y":[["G0",0 ,27],["G1",10,13],["G1",10,0 ],["G0",10,13],["G1",20,27]],
"Z":[["G0",0 ,27],["G1",20,27],["G1",0 ,0 ],["G1",20,0]],
"-":[["G0",0 ,13],["G1",10,13]]}





if __name__ == "__main__":


    position = Position()
    position.set_current_pos(0,0)
    position.draw_text("M", 1.0)
    position.drive_to(0,0)
    position.draw_gcode(["G03",0,50,None, 0, 25])

        
    
