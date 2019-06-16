import mxnet as mx
import numpy as np
import time
import cv2, os, urllib
from collections import namedtuple

class Prediction_Unit():
	def __init__(self, logger):
		self.logger = logger
		self.Batch = namedtuple('Batch', ['data'])
		
		with open('synset.txt', 'r') as f:
			self.synsets = [l.rstrip() for l in f]
			
		self.sym, self.arg_params, self.aux_params = mx.model.load_checkpoint('Inception-BN', 126)
		
		self.mod = mx.mod.Module(symbol=self.sym, context=mx.cpu())
		self.mod.bind(for_training=False, data_shapes=[('data', (1,3,224,224))])
		self.mod.set_params(self.arg_params, self.aux_params)
		
	def predict(self, filename, mod, synsets, N=5):
		tic = time.time()
		img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
		if img is None:
			return None
		img = cv2.resize(img, (224, 224))
		img = np.swapaxes(img, 0, 2)
		img = np.swapaxes(img, 1, 2)
		img = img[np.newaxis, :]
		self.logger.info("Image pre-processed with OpenCV API in {}".format(str(time.time()-tic)))
		toc = time.time()
		mod.forward(self.Batch([mx.nd.array(img)]))
		prob = self.mod.get_outputs()[0].asnumpy()
		prob = np.squeeze(prob)
		self.logger.info("forward pass in {}".format(str(time.time()-toc)))


		topN = []
		a = np.argsort(prob)[::-1]
		for i in a[0:N]:
			# self.logger.info('probability=%f, class=%s' %(prob[i], synsets[i]))
			topN.append((prob[i], self.synsets[i]))
		return topN
		
	def predict_from_url(self, url, N=5):
		filename = url.split("/")[-1]
		urllib.urlretrieve(url, filename)
		img = cv2.imread(filename)
		if img is None:
			self.logger.info("Image not downloaded or error")
		else:
			return self.predict(filename, self.mod, self.synsets, N)
			
	def predict_from_local_file(self, filename, N=5):
		return self.predict(filename, self.mod, self.synsets, N)
