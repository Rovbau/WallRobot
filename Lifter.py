from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

class Lifter():
    def __init__(self, PIN):
        
        self.PIN = PIN
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN,GPIO.OUT)
        GPIO.output(self.PIN, False)

        self.command_old = "UP"

    def goto(self, command):
        if command.upper() == "UP":
            GPIO.output(self.PIN, True)
        else:
            GPIO.output(self.PIN, False)

        if command != self.command_old:
            sleep(0.1)
            self.command_old = command


if __name__ == "__main__":

    lifter = Lifter(29)
    lifter.goto("up")
    sleep(2)
    lifter.goto("down")
