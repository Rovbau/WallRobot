from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

class Lifter():
    def __init__(self, PIN):
        
        self.PIN = PIN
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN,GPIO.OUT)
        GPIO.output(self.PIN, False)

    def goto(self, command):
        if command.upper() == "UP":
            GPIO.output(self.PIN, True)
        else:
            GPIO.output(self.PIN, False)


if __name__ == "__main__":

    lifter = Lifter()
    lifter.goto("up")
    sleep(2)
    lifter.goto("down")
