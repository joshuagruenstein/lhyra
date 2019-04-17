from abc import ABC, abstractmethod

# An example of a parameter type.
class GradientParameter:
	def __init__(self, _min=None, _max=None):
		self.min = _min
		self.max = _max

class Solver:
	# Instantiate a solver given a dictionary of abstract parameters
	# and an evaluation method with the following signature:
	# f(data, recursive_hook, parameter_dict) -> data
	def __init__(self, method, abstract_parameters):
		self.parameters = abstract_parameters
		self.method = methods

	# Given a dictionary of parameters, return a function of
	# signature f(data, recursive_hook) -> data
	def parametrized(self, parameters):
		return lambda data, hook: self.method(data, hook, parameters)

class Data(ABC):
	# Return a randomly sampled data batch of batch_size.
	@abstractmethod
	def get_data(self, batch_size):
		pass

class FeatureExtractor(ABC):
	# Get the output shape of the feature extractor.
	# Might also be useful to also give type data here, 
	# (eg class vs gradient value, scaled vs unscalled,
	# could use Parameter type for this?)
	@property
	@abstractmethod
	def shape(self):
		pass

	# Call extractor on given data.
	@abstractmethod
	def __call__(self, data):
		pass

class Optimizer(ABC):
	# Initialize an optimizer object.
	@abstractmethod
	def __init__(self, solvers, data, extractor):
		pass

	# Train the classifier on the data.
	@abstractmethod
	def train(self):
		pass

	# Pick and parametrize a solver from the bag of solvers.
	@abstractmethod
	def solver(self, features):
		pass

class Lhyra:
	# To instantiate a Lhyra instance we pass in a list/set of
	# Solver objects, a Data object, a FeatureExtractor subclass,
	# and an Optimizer subclass.
	def __init__(self, solvers, data, extractor, optimizer):
		self.extractor = extractor
		self.optimizer = optimizer(solvers, data, extractor)

	# Train the already instantiated optimizer.
	def train(self):
		self.optimizer.train()

	# Eval on data. Ask the optimizer to pick and parametrize a solver
	# given a set of features, then evaluate it on the data, providing
	# a hook back into this method for recursive subcalls. 
	def eval(self, data):
		return self.optimizer.solver(self.extractor(data))(data,self.eval)



