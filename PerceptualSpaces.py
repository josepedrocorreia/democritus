import numpy as np
from scipy import stats as stats

class PerceptualSpace:
    
    def __init__(self, number_of_states, start=0, end=1):
        self.state_space = np.linspace(start, end, number_of_states, endpoint=False)
        self.distance_matrix = np.array([[ abs(x - y)
                                         for y in self.state_space ]
                                        for x in self.state_space ])
        
class UniformPerceptualSpace(PerceptualSpace):
    
    def __init__(self, number_of_states, start=0, end=1):
        PerceptualSpace.__init__(self, number_of_states, start, end)
        self.prior_distribution = stats.uniform.pdf(self.state_space, scale=len(self.state_space))
        
class NormalPerceptualSpace(PerceptualSpace):

    def __init__(self, number_of_states, start=0, end=1, center=0.5, standard_deviation=0.1):
        PerceptualSpace.__init__(self, number_of_states, start, end)
        self.prior_distribution = stats.norm.pdf(self.state_space, loc=center, scale=standard_deviation)
