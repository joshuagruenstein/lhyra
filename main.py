from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List


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
    def get_data(self, batch_size: int) -> List[Any]:
        """
        Return a randomly sampled data batch of batch_size.
        :param batch_size: The amount of data returned.
        :return: A list of data.
        """
        pass


class Solver:
    def __init__(self,
                 method: Callable[[DataStore,
                                   Callable,
                                   Dict[str, Any]], DataStore],
                 abstract_parameters: Dict[str, Any]):
        """
        Instantiate a solver.
        :param method: A recursive evaluation method.
        :param abstract_parameters: A dict of parameter names to types.
        """
        self.method = method
        self.parameters = abstract_parameters

    def parametrized(self, parameters: Dict[str, Any]) -> \
            Callable[[DataStore, Callable], DataStore]:
        """
        Parametrizes self.method.
        :param parameters: A dict of parameters to values.
        :return: A a function which calls self.method with parameters applied.
        """
        return lambda data_store, hook: self.method(data_store,
                                                    hook,
                                                    parameters)


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
    def __call__(self, data: Any) -> List[Any]:
        """
        Call extractor on given data.
        :param data: A piece of data to extract the parameters of.
        :return: Floats between 0 and 1 of shape self.shape.
        """
        pass


class Optimizer(ABC):
    @abstractmethod
    def __init__(self,
                 solvers: List[Solver],
                 data_store: DataStore,
                 extractor: FeatureExtractor):
        """
        Initialize an optimizer.
        :param solvers: A list of potential solvers.
        :param data_store: A DataStore which generates representative data.
        :param extractor: An extractor which generates informative features.
        """
        pass

    @abstractmethod
    def train(self, eval_method):
        """
        Train the classifier on the data, given a hook into
        the Lhyra object's eval method.
        :param eval_method: Eval method of the associated Lhyra object.
        """
        pass

    @abstractmethod
    def solver(self, features: List[Any]) -> Solver:
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
        self.optimizer = optimizer(solvers, data_store, extractor)

    def train(self):
        """
        Train the already instantiated optimizer.
        """
        self.optimizer.train(self.eval)

    def eval(self, data: Any) -> Any:
        """
        Eval on data. Ask the optimizer to pick and parametrize a solver
        given a set of features, then evaluate it on the data, providing
        a hook back into this method for recursive subcalls.
        :param data: The data to evaluate on.
        :return: A solution.
        """
        return self.optimizer.solver(self.extractor(data))(data, self.eval)
