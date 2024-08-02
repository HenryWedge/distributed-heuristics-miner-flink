from abc import abstractmethod, ABC


class ModelSource(ABC):
    @abstractmethod
    def get_petri_net(self):
        pass
