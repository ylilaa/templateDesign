from dataclasses import dataclass, field
from datetime import datetime
from calendar import isleap
from dateutil.relativedelta import relativedelta
from utils import get_days_in_year

@dataclass(slots=True)
class Bond():
    """Bond dataclass. Holds all the useful properties to type the bond for the correct pricing algorithm"""
    emission : str
    dateValo : str
    echeance : str
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
        self.mrr = (datetime.strptime(self.echeance, '%Y-%m-%d') - datetime.strptime(self.dateValo, '%Y-%m-%d')).days
        self.mi = (datetime.strptime(self.echeance, '%Y-%m-%d') - datetime.strptime(self.emission, '%Y-%m-%d')).days
        self.leap = get_days_in_year(self.dateValo)
        # set dates
        delta =  relativedelta(years=1)
        _ = datetime.strptime(self.echeance, '%Y-%m-%d')
        dates = [_]
        while _ > datetime.strptime(self.emission, '%Y-%m-%d'):
            _ -= delta
            if _ > datetime.strptime(self.emission, '%Y-%m-%d'):
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
