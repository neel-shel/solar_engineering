import sys
import numpy as np
from solar_radiation import SolarRadiation
from solar_parameters import SolarParameters
from daily_integration import DailyIntegration
from cpr import CPR
from cprg import CPRG
from lj import LJ
from __init__ import calculate_local_standard_meridian, calculate_n, time_to_hour_angle

class SolarEstimation:
    def __init__(self, model_name, latitude, delta_s, h_s, h_ss, H_bar_h, H_bar_d, extraterrestrial_radiation_factor, beta, rho, i):
        self.model_name = model_name
        if model_name == "daily_integration":
            daily_integration = DailyIntegration(latitude, delta_s, h_s, h_ss, H_bar_h, extraterrestrial_radiation_factor)
            self.r_d = daily_integration.r_d
            self.r_t = daily_integration.r_t
        elif model_name == "cpr":
            cpr = CPR(h_s, h_ss)
            self.r_d = cpr.r_d
            self.r_t = cpr.r_t
        elif model_name == "cprg":
            cprg = CPRG(h_s, h_ss)
            self.r_d = cprg.r_d
            self.r_t = cprg.r_t
        else:
            raise ValueError(f"Unsupported model: {model_name}")
        print(self.r_t*H_bar_h-self.r_d*H_bar_d, np.cos(np.radians(i))/np.sin(np.radians(alpha)))
        self.I_b_c = (self.r_t*H_bar_h-self.r_d*H_bar_d)*np.cos(np.radians(i))/np.sin(np.radians(alpha))
        self.I_d_c = self.r_d*H_bar_d*np.square(np.cos(np.radians(beta/2)))
        self.I_r_c = rho*self.r_t*H_bar_h*np.square(np.sin(np.radians(beta/2)))
        print(f"I_b_c: {self.I_b_c} I_d_c: {self.I_d_c} I_r_c: {self.I_r_c}")
        self.I_c = self.I_b_c + self.I_d_c + self.I_r_c


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(r"python src\utils\solar_estimation.py <MODEL_NAME>")
        sys.exit(1)
    model_name = sys.argv[1]
    ground_type = 'ordinary'
    input_date = "Mar 21"
    latitude = 36.08
    longitude = 115.16
    beta = latitude
    a_w = 0
    tau_b = 0.355
    tau_d = 2.211
    H_bar_h = 5.24e3
    H_bar_d = 1.26e3

    n = calculate_n(input_date)

    # Calculate Local Standard Meridian (LST) based on longitude
    l_st = calculate_local_standard_meridian(longitude)
    
    # Example Local Standard Time (LST) (format "YYYY-MM-DD HH:MM:SS")
    LST = "2025-03-21 12:00:00"
    
    solar_parameters = SolarParameters(n, latitude, longitude, LST, l_st)
    alpha = solar_parameters.alpha
    delta_s = solar_parameters.delta_s
    h_s = solar_parameters.h_s
    h_ss = solar_parameters.h_ss
    print(h_s, h_ss)
    h_ss = time_to_hour_angle(h_ss)
    a_s = solar_parameters.a_s
    solar_radiation = SolarRadiation(n, alpha, tau_b, tau_d, beta, a_s, a_w, ground_type = ground_type)
    extraterrestrial_radiation_factor = solar_radiation.extra_terrestrial_radiation_factor
    i = solar_radiation.i
    rho = solar_radiation.rho
    # if len(sys.argv) == 1:
    #     solar_estimation_daily_integration = SolarEstimation("daily_integration", latitude, delta_s, h_s, h_ss, H_bar_h, extraterrestrial_radiation_factor)
    #     solar_estimation_cpr = SolarEstimation("cpr", latitude, delta_s, h_s, h_ss, H_bar_h, extraterrestrial_radiation_factor)
    #     solar_estimation_cprg = SolarEstimation("cprg", latitude, delta_s, h_s, h_ss, H_bar_h, extraterrestrial_radiation_factor)
    solar_estimation = SolarEstimation(model_name, latitude, delta_s, h_s, h_ss, H_bar_h, H_bar_d, extraterrestrial_radiation_factor, beta, rho, i)
    print(f"Model: {model_name} I_c: {solar_estimation.I_c}")