import re
from abc import ABC, abstractmethod
from data import Bond


class PricerBase(ABC):
    """
    The Abstract Class defines a template method that contains a skeleton of
    some algorithm, composed of calls to (usually) abstract primitive
    operations.

    Concrete subclasses should implement these operations, but leave the
    template method itself intact.
    """

    def template_method(self, bond : Bond) -> float:
        """
        The template method defines the skeleton of the algorithm.
        """
        
        return self.get_valo(bond)
    
    @abstractmethod
    def get_valo(self, bond : Bond) -> float:
        pass

