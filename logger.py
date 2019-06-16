import logging

FORMAT = '%(asctime)-15s %(message)s'
logger = None

class Logger():
	def __init__(self):
		global logger
		if logger is None:
			logging.basicConfig(format=FORMAT)
			logger = logging.getLogger('Bicycle safety system')
			logger.setLevel(logging.DEBUG)
			logger.info("Logger initialised")
	def get_logger(self):
		global logger
		return logger
