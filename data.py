from dataclasses import dataclass, field
from datetime import datetime
from calendar import isleap
from dateutil.relativedelta import relativedelta
from utils import get_days_in_year

@dataclass(slots=True)
class Bond():
    """Bond dataclass. Holds all the useful properties to type the bond for the correct pricing algorithm"""
    emission : datetime
    dateValo : datetime
    echeance : datetime
    facial : float
    ytm : float
    nominal : float
    dates : list = field(init=False)
    mrr : int = field(init=False)
    mi : int = field(init=False)
    leap : int = field(init=False)
    type : str = field(init=False)
    
    def __post_init__(self) -> None:
        # set MRR Mi and leap
        self.mrr = (self.echeance - self.dateValo).days
        self.mi = (self.echeance - self.emission).days
        self.leap = get_days_in_year(self.dateValo)
        # set dates
        delta =  relativedelta(years=1)
        _ = self.echeance
        dates = [_]
        while _ > self.emission:
            _ -= delta
            if _ > self.emission:
                dates.append(_)
        self.dates = dates
        # Get type
        if self.mi < self.leap:
            self.type = 'A'
        else:
            if self.mrr < self.leap : 
                self.type = 'B'
            if len(self.dates) == 1 and self.mi > self.leap and self.mrr < self.leap:
                self.type = 'D'
            if len(self.dates) != 1 and self.mi > self.leap and self.mrr < self.leap :
                self.type = 'E'
            else:         
                self.type = 'C'
