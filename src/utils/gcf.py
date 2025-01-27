import numpy as np

class GCF:
    def __init__(self, R, r, L):
        self.R = R
        self.r = r
        self.L = L

        self.limit_angle = np.degrees(np.arctan((self.R+self.r)/self.L))
        self.opening_angle = np.degrees(np.arctan((self.R)/self.L))
        self.slope_angle = np.degrees(np.arctan((self.R-self.r)/self.L))
