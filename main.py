from bicycle_detector.prediction_unit import Prediction_Unit
from remote_control.remote_control_unit import Remote_Control_Unit
from logger import Logger

import sys
import picamera

bicycle_symbols = ["n03792782",
				   "n02835271",
				   "n03791053",
				   "n03785016",
				   "n04509417",
				   "n04482393"]

def main():

	logger = Logger().get_logger()
	camera = picamera.PiCamera()
	predictor = Prediction_Unit(logger)
	remote = Remote_Control_Unit(logger)
	
        if "lock" in sys.argv:
            remote.lock()
            return
        if "unlock" in sys.argv:
            remote.unlock()
            return
        
        if "local" in sys.argv:
			path = sys.argv[2]
			logger.info("starting prediction")
			topn = predictor.predict_from_local_file(path, N=5)
			logger.info("prediction done")
			bicycle_detected = False
			for detection in topn:
				for desired_symbol in bicycle_symbols:
					if desired_symbol in detection[1]:
						logger.warning("Bicycle detected")
						bicycle_detected = True
				if bicycle_detected:
					remote.lock()
					break
			if not bicycle_detected:
				logger.info("Road is clear")
			return

	while True:
		logger.info("starting capture")
		filename = '/home/pi/cap.jpg'
		camera.capture(filename)
		logger.info("capture done")

		logger.info("starting prediction")
		topn = predictor.predict_from_local_file(filename, N=5)
		logger.info("prediction done")
		
		bicycle_detected = False
		for detection in topn:
			for desired_symbol in bicycle_symbols:
				if desired_symbol in detection[1]:
					logger.warning("Bicycle detected")
					bicycle_detected = True
			if bicycle_detected:
				remote.lock()
				break
				
		if not bicycle_detected:
			logger.info("Road is clear")	
			
		
if __name__ == "__main__":
	main()

