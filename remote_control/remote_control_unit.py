import RPi.GPIO as GPIO
import time

LOCK_PIN = 17
UNLOCK_PIN = 18

class Remote_Control_Unit():
        def __init__(self, logger):            
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(LOCK_PIN, GPIO.OUT)
            GPIO.setup(UNLOCK_PIN, GPIO.OUT)
            self.logger = logger
        
        def lock(self):
            logger.warning("Locking the car")
            GPIO.output(LOCK_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(LOCK_PIN, GPIO.LOW)
            logger.warning("Locking done")
        
        def unlock(self):
            logger.warning("Unlocking the car")
            GPIO.output(UNLOCK_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(UNLOCK_PIN, GPIO.LOW)
            logger.warning("Unlocked the car")
        
        def action(self, action):
            if action == "lock":
                self.lock()
            elif action == "unlock":
                self.unlock()
            else:
                print("Wrong action: %".format(action))


                
            
