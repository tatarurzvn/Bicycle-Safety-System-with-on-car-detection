import logging

FORMAT = '%(asctime)-15s %(message)s'
logger = None
logname = "/home/pi/Desktop/logs.log"
class Logger():
	def __init__(self):
		global logger
		if logger is None:
			logging.basicConfig(filename=logname,
                                            filemode='a',
                                            format=FORMAT)
			logger = logging.getLogger('Bicycle safety system')
			logger.setLevel(logging.DEBUG)
			logger.info("Logger initialised")
	def get_logger(self):
		global logger
		return logger
