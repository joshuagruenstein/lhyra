from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List
from time import time


class GradientParameter:
    """
    A sample parameter.
    """
    def __init__(self, _min: float = None, _max: float = None):
        """
        Initiate a GradientParameter.
        :param _min: The minimum value of the parameter.
        :param _max: The maximum value of the parameter.
        """
        self.min = _min
        self.max = _max


class DataStore(ABC):
    @abstractmethod
    def get_data(self, batch_size: int) -> List:
        """
        Return a randomly sampled data batch of batch_size.
        :param batch_size: The amount of data returned.
        :return: A list of data.
        """
        pass


class DataGenerator(DataStore):
    def __init__(self, method: Callable[[int], List]):
        """
        Create a data generator given a function that takes a batch
        size and returns a bunch of datum.
        :param method: The data generation method.
        """
        self.method = method

    def get_data(self, batch_size: int) -> List:
        """
        Return a randomly sampled data batch of batch_size.
        :param batch_size: The amount of data returned.
        :return: A list of data.
        """

        return [self.method() for _ in range(batch_size)]


class Solver:
    def __init__(self,
                 method: Callable[[Any,
                                   Callable,
                                   Dict[str, Any]], Any],
                 abstract_parameters: Dict[str, Any]):
        """
        Instantiate a solver.
        :param method: A recursive evaluation method.
        :param abstract_parameters: A dict of parameter names to types.
        """
        self.method = method
        self.parameters = abstract_parameters

    def parametrized(self, parameters: Dict[str, Any]) -> \
            Callable[[Any, Callable], Any]:
        """
        Parametrizes self.method.
        :param parameters: A dict of parameters to values.
        :return: A a function which calls self.method with parameters applied.
        """
        return lambda data, hook: self.method(data, hook, parameters)

    def __repr__(self):
        """
        Pretty printer.
        :return: A string representation of the solver.
        """

        return "<Solver: " + self.method.__name__ + ">"


class FeatureExtractor(ABC):
    """
    Given data, produces a set of features normalized between 0 and 1.
    """
    @property
    @abstractmethod
    def shape(self) -> List[int]:
        """
        Get the output shape of the feature extractor.
        :return: A list of integers representing the output's dimensions.
        """
        pass

    @abstractmethod
    def __call__(self, data: Any) -> List:
        """
        Call extractor on given data.
        :param data: A piece of data to extract the parameters of.
        :return: Floats between 0 and 1 of shape self.shape.
        """
        pass


class Optimizer(ABC):
    def __init__(self,
                 lhyra: 'Lhyra'):
        """
        Initialize an optimizer.
        :param solvers: A list of potential solvers.
        :param data_store: A DataStore which generates representative data.
        :param extractor: An extractor which generates informative features.
        """
        
        self.lhyra = lhyra

    @abstractmethod
    def train(self):
        """
        Train the classifier on the data.
        """
        pass

    @abstractmethod
    def solver(self, features: List) -> Solver:
        """
        Pick and parametrize a solver from the bag of solvers.
        :param features: Features provided to inform solver choice.
        :return: The Solver best suited given the features provided.
        """
        pass


class Lhyra:
    def __init__(self,
                 solvers: List[Solver],
                 data_store: DataStore,
                 extractor: FeatureExtractor,
                 optimizer: Optimizer):
        """
        Instantiate a Lhyra instance.
        :param solvers: A list of potential solvers.
        :param data_store: A DataStore which generates representative data.
        :param extractor: An extractor which generates informative features.
        :param optimizer: An untrained optimizer.
        """
        self.extractor = extractor
        self.data_store = data_store
        self.solvers = solvers
        self.times = []
        self.vocal = False

        self.optimizer = optimizer(self)

        self.train = self.optimizer.train

    def clear(self):
        """
        Clear training metadata from Lhyra instance, eg self.times.
        """

        self.times.clear()

    def eval(self, data: Any, vocal: bool=False) -> Any:
        """
        Eval on data. Ask the optimizer to pick and parametrize a solver
        given a set of features, then evaluate it on the data, providing
        a hook back into this object for recursive subcalls.
        :param data: The data to evaluate on.
        :return: A solution.
        """

        if vocal:
            self.vocal = True

        time_slot = len(self.times)

        self.times.append(None)

        optimizer_start = time()
        solver = self.optimizer.solver(self.extractor(data))
        optimizer_end = time()
        start_time = time()

        sol, overhead = solver(data, self.eval)

        self.times[time_slot] = time() - start_time - overhead

        if vocal:
            self.vocal = False

        return sol, overhead + optimizer_end - optimizer_start
