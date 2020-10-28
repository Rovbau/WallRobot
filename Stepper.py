import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)

class Stepper():
    """Controls a Stepper Motor with the Modul A4988"""
    def __init__(self, name, mm_per_step, pin_dir, pin_step):
        self.name = name
        self.mm_per_step = mm_per_step
        self.pin_dir = pin_dir
        self.pin_step = pin_step
        self.actual_steps = 0
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_dir,GPIO.OUT)
        GPIO.setup(pin_step,GPIO.OUT)
        GPIO.output(pin_dir, False)
        GPIO.output(pin_step, False)

    def get_actual_steps(self):
        """Get the actual Motor Position"""
        return(self.name, self.actual_steps)

    def set_actual_steps(self, actual_steps):
        """Set the actual Motor Position"""
        self.actual_steps = actual_steps
        
    def goto_pos(self, lenght):
        """Set Motor to desired position. Input: lentht[mm]"""
        steps = int(lenght / self.mm_per_step)
        while steps != self.actual_steps:
            if steps > self.actual_steps:
                self.do_step(1)
                self.actual_steps += 1
            else:
                self.do_step(-1)
                self.actual_steps -= 1
            
    def do_step(self, steps, speed = 0.01):
        """Do Motor Steps. +steps or -steps changes direction)"""
        if steps >= 0:
            GPIO.output(self.pin_dir, True)
        else:
            print("minus")
            GPIO.output(self.pin_dir, False)
        for x in range(abs(steps)):
            print("step")
            GPIO.output(self.pin_step, True)
            sleep(speed)
            GPIO.output(self.pin_step, False)


if __name__ == "__main__":
    
    stepper1 = Stepper("Left", mm_per_step = 1, pin_dir = 23, pin_step = 24)
    stepper1.goto_pos(-1)
    print(stepper1.get_actual_steps())
