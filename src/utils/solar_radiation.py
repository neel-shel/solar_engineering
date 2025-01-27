import numpy as np
from datetime import datetime, timedelta
from solar_parameters import SolarParameters

def days_from_jan(input_date):
    current_year = datetime.now().year
    date = datetime.strptime(f"{input_date} {current_year}", "%b %d %Y")
    jan_1 = datetime(year=current_year, month=1, day=1)
    delta = date - jan_1
    print(f"Days from January 1st to {input_date}: {delta.days + 1}")
    return delta.days + 1  # Include Jan 1 as day 1

class SolarRadiation:
    def __init__(self, n, alpha, tau_b, tau_d, beta, a_s, a_w, ground_type='ordinary', I0=1367):
        print(f"Initializing SolarRadiation with parameters:\n n: {n}, alpha: {alpha}, tau_b: {tau_b}, tau_d: {tau_d}, beta: {beta}, a_s: {a_s}, a_w: {a_w}, ground_type: {ground_type}, I0: {I0}")
        
        self.n = n
        self.I0 = I0
        self.alpha = alpha
        self.tau_b = tau_b
        self.tau_d = tau_d
        self.beta = beta
        self.ground_type = ground_type
        self.a_s = a_s
        self.a_w = a_w
        
        # Set ground reflectivity (rho)
        assert self.ground_type == 'ordinary' or self.ground_type == 'snow'
        if self.ground_type == 'ordinary':
            self.rho = 0.2
        else:
            self.rho = 0.8
        
        print(f"Ground reflectivity (rho): {self.rho}")

        # Solar incidence angle (i)
        self.i = np.degrees(np.arccos((np.cos(np.radians(self.alpha)) * np.cos(np.radians(self.a_s - self.a_w)) * np.sin(np.radians(self.beta)) + np.sin(np.radians(self.alpha)) * np.cos(np.radians(self.beta)))))
        print(f"Solar incidence angle (i): {self.i}")

        # Parameters for extraterrestrial radiation calculation
        self.a0 = 1.00011
        self.a1 = 0.034221
        self.a2 = 0.00128
        self.a3 = 0.000719
        self.a4 = 0.000077
        x = 360 * (self.n - 1) / 365
        print(f"x (angle for extraterrestrial radiation): {x}")
        
        self.extra_terrestrial_radiation_factor = (self.a0 + self.a1 * np.cos(np.radians(x)) + self.a2 * np.sin(np.radians(x)) + self.a3 * np.cos(np.radians(2 * x)) + self.a4 * np.sin(np.radians(2 * x)))
        print(f"Extra-terrestrial radiation factor: {self.extra_terrestrial_radiation_factor}")

        self.I = self.extra_terrestrial_radiation()
        print(f"Extra-terrestrial solar radiation (I): {self.I}")

        self.I_c = self.terrestrial_solar_radiation()
        print(f"Terrestrial solar radiation (I_c): {self.I_c}")

    def extra_terrestrial_radiation(self):
        I = self.I0 * self.extra_terrestrial_radiation_factor
        print(f"Calculating extra-terrestrial radiation: {I}")
        return I
    
    def terrestrial_solar_radiation(self):
        print("Calculating terrestrial solar radiation...")
        m = 1 / (np.sin(np.radians(self.alpha)) + np.power((6.07995 + self.alpha), (-1.6364)))
        print(f"Air mass (m): {m}")
        
        b0 = 1.219
        b1 = -0.043
        b2 = -0.151
        b3 = -0.204
        d0 = 0.202
        d1 = 0.852
        d2 = -0.007
        d3 = -0.357
        
        b = b0 + b1 * self.tau_b + b2 * self.tau_d + b3 * self.tau_b * self.tau_d
        d = d0 + d1 * self.tau_b + d2 * self.tau_d + d3 * self.tau_b * self.tau_d
        print(f"b: {b}, d: {d}")
        
        I_b_N = self.I * np.exp(-self.tau_b * np.power(m, b))
        print(f"Beam normal radiation (I_b_N): {I_b_N}")
        
        I_d_h = self.I * np.exp(-self.tau_d * np.power(m, d))
        print(f"Diffuse horizontal radiation (I_d_h): {I_d_h}")
        
        I_h = I_b_N * np.sin(np.radians(self.alpha)) + I_d_h
        print(f"Total radiation (I_h): {I_h}")
        
        I_r_c = I_h * self.rho * (1 - np.cos(np.radians(self.beta))) / 2
        print(f"Reflected radiation (I_r_c): {I_r_c}")
        
        I_d_c = I_d_h * (1 + np.cos(np.radians(self.beta))) / 2
        print(f"Diffuse component with ground (I_d_c): {I_d_c}")
        
        I_b_c = I_b_N * (np.cos(np.radians(self.alpha)) * np.cos(np.radians(self.a_s - self.a_w)) * np.sin(np.radians(self.beta)) + np.sin(np.radians(self.alpha)) * np.cos(np.radians(self.beta)))
        print(f"Beam component with ground (I_b_c): {I_b_c}")

        I_c = I_b_c + I_d_c + I_r_c
        print(f"Total terrestrial solar radiation (I_c): {I_c}")

        return I_c

if __name__ == "__main__":
    input_date = "Feb 1"
    n = days_from_jan(input_date)
    
    # Example coordinates for Gainesville, Florida
    latitude = 27.96
    longitude = 82.54
    
    # Local Standard Meridian (LST) is typically a multiple of 15 degrees, for example 75°W for Eastern Standard Time
    l_st = 75  # Local Standard Meridian (EST is 75°W, meaning UTC-5)
    
    # Example Local Standard Time (LST) (format "YYYY-MM-DD HH:MM:SS")
    LST = "2025-02-01 12:00:00"
    
    solar_parameters = SolarParameters(n, latitude, longitude, LST, l_st)
    alpha = solar_parameters.alpha
    a_s = solar_parameters.a_s
    tau_b = 0.35109
    tau_d = 2.48558
    solar_radiation = SolarRadiation(n, alpha, tau_b, tau_d, 30, a_s, 10)

    print(f"Solar radiation (I_c): {solar_radiation.I_c} W/m^2")
