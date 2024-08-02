from abc import abstractmethod, ABC

class EventLogSource(ABC):
    @abstractmethod
    def get_event_log(self):
        pass
