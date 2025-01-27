import numpy as np
from solar_radiation import SolarRadiation
from solar_parameters import SolarParameters
from __init__ import calculate_local_standard_meridian, calculate_n, time_to_hour_angle

class LJ:
    def __init__(self, L, alpha, h_sr, h_ss, delta_s, beta, H_bar_h, H_o_bar_h, i, z, rho, sky_type="isotropic"):
        """
        H_bar_h: horizontal terrestrial radiation per month
        H_o_bar_h: horizontal extraterrestrial radiation per month
        h_ss: sunset hour angle
        """
        print("Initializing LJ class...")
        self.H_bar_h = H_bar_h
        self.H_o_bar_h = H_o_bar_h
        self.h_sr = h_sr
        self.h_ss = h_ss
        self.L = L
        self.i = i
        self.z = z
        self.alpha = alpha
        self.beta = beta
        self.delta_s = delta_s
        self.sky_type = sky_type

        # Debugging prints for each initialization parameter
        print(f"L: {L}, alpha: {alpha}, h_sr: {h_sr}, h_ss: {h_ss}, delta_s: {delta_s}, beta: {beta}")
        print(f"H_bar_h: {H_bar_h}, H_o_bar_h: {H_o_bar_h}, rho: {rho}, sky_type: {sky_type}")

        # Call the methods to calculate various parameters
        self.MCI = self.monthly_clearness_index()
        self.DTR = self.diffuse_to_total_radiation_ratio()
        self.B_bar_h = self.H_bar_h * (1 - self.DTR)
        self.D_bar_h = self.H_bar_h - self.B_bar_h
        
        print(f"Monthly Clearness Index (MCI): {self.MCI}")
        print(f"Diffuse to Total Radiation Ratio (DTR): {self.DTR}")
        print(f"B_bar_h (average beam horizontal radiation): {self.B_bar_h}")
        print(f"D_bar_h (average diffuse horizontal radiation): {self.D_bar_h}")

        self.h_sr_0 = -np.degrees(np.arccos(-np.tan(np.radians(self.L)) * np.tan(np.radians(self.delta_s))))
        self.h_sr_0_deg = self.h_sr_0
        self.h_sr_0_rad = self.h_sr_0_deg / 180 * np.pi
        self.h_ss_0 = -self.h_sr_0
        print(f"Calculated h_sr_0: {self.h_sr_0}, h_sr_0_deg: {self.h_sr_0_deg}, h_sr_0_rad: {self.h_sr_0_rad}, h_ss_0: {self.h_ss_0}")

        self.BRTF = self.beam_radiation_tilt_factor()
        print(f"Beam Radiation Tilt Factor (BRTF): {self.BRTF}")
        
        self.B_bar_c = self.BRTF * self.B_bar_h
        self.DRTF = self.diffuse_radiation_tilt_factor()
        self.RRTF = rho * np.square(np.sin(np.radians(self.beta / 2)))
        
        print(f"B_bar_c (tilted monthly average beam radiation): {self.B_bar_c}")
        print(f"Diffuse Radiation Tilt Factor (DRTF): {self.DRTF}")
        print(f"Reflected Radiation Tilt Factor (RRTF): {self.RRTF}")

        self.H_bar_c = (self.BRTF + self.RRTF) * self.B_bar_h + (self.DRTF + self.RRTF) * self.DTR * H_bar_h
        print(f"Calculated H_bar_c (average tilted radiation): {self.H_bar_c}")

    def monthly_clearness_index(self):
        print("Calculating Monthly Clearness Index (MCI)...")
        mci = np.divide(self.H_bar_h, self.H_o_bar_h)
        print(f"MCI: {mci}")
        return mci
    
    def diffuse_to_total_radiation_ratio(self, type="cpr"):
        print(f"Calculating Diffuse to Total Radiation Ratio with method: {type}...")
        h_ss_rad = np.radians(self.h_ss)
        if type == "empirical":
            a0 = 1.390
            a1 = -4.027
            a2 = 5.531
            a3 = -3.108
            temp = a0 + a1 * self.MCI + a2 * self.MCI**2 + a3 * self.MCI**3
        elif type == "cpr":
            temp = 0.775 + 0.347 * (h_ss_rad - np.pi / 2) - (0.505 + 0.0261 * (h_ss_rad - np.pi / 2)) * np.cos(2 * self.MCI - np.pi / 2)
        
        # print(f"Diffuse to Total Radiation Ratio (DTR): {temp}")
        return temp

    def beam_radiation_tilt_factor(self, type='monthly'):
        print(f"Calculating Beam Radiation Tilt Factor with method: {type}...")
        if type == 'monthly':
            temp = np.divide(
                (np.cos(np.radians(self.L - self.beta)) *
                 np.cos(np.radians(self.delta_s)) *
                 np.sin(np.radians(self.h_sr)) + 
                 (np.radians(self.h_sr)) *
                 np.sin(np.radians(self.L - self.beta)) *
                 np.sin(np.radians(self.delta_s))),
                (np.cos(np.radians(self.L)) *
                 np.cos(np.radians(self.delta_s)) *
                 np.sin(self.h_sr_0_rad) + 
                 self.h_sr_0_rad *
                 np.sin(np.radians(self.L)) *
                 np.sin(np.radians(self.delta_s)))
            )
        
        # print(f"Beam Radiation Tilt Factor (BRTF): {temp}")
        return temp
    
    def diffuse_radiation_tilt_factor(self):
        temp = np.square(np.cos(np.radians(self.beta / 2)))
        if self.sky_type == "isotropic":
            return temp
        elif self.sky_type == "anisotropic" or self.sky_type == "circumsolar":
            F = 1-np.square(np.divide(self.D_bar_h), self.H_bar_h)
            M1 = 1 + F*np.square(np.sin(np.radians(self.beta / 2)))
            M2 = 1 + F*np.square(np.cos(np.radians(self.i)))*np.sin(np.radians(self.z))**3
            return temp * M1 * M2
if __name__ == "__main__":
    ground_type = 'ordinary'
    input_date = "Jan 16"
    n = calculate_n(input_date)
    
    latitude = 25
    longitude = 82.54
    
    # Local Standard Meridian (LST) is typically a multiple of 15 degrees, for example 75°W for Eastern Standard Time
    l_st = calculate_local_standard_meridian(longitude)  # Local Standard Meridian (EST is 75°W, meaning UTC-5)
    
    # Example Local Standard Time (LST) (format "YYYY-MM-DD HH:MM:SS")
    LST = "2025-01-16 12:00:00"
    
    solar_parameters = SolarParameters(n, latitude, longitude, LST, l_st)
    alpha = solar_parameters.alpha
    delta_s = solar_parameters.delta_s
    a_s = solar_parameters.a_s
    z = solar_parameters.z
    h_sr = solar_parameters.h_sr
    h_ss = solar_parameters.h_ss
    h_sr = time_to_hour_angle(h_sr)
    h_ss = time_to_hour_angle(h_ss)
    print(h_sr, h_ss)
    tau_b = 0.35109
    tau_d = 2.48558
    solar_radiation = SolarRadiation(n, alpha, tau_b, tau_d, 30, a_s, 10, ground_type=ground_type)
    i = solar_radiation.i
    beta = solar_radiation.beta
    rho = solar_radiation.rho


    print(f"{solar_radiation.I_c} W/m^2")
    H_bar_h = 16215
    H_o_bar_h = 24199
    lj_model = LJ(latitude, 0, h_sr, h_ss, delta_s, beta, H_bar_h, H_o_bar_h, i, z, rho)
    total_long_term_radiation = lj_model.H_bar_c
    print(f"Total Long Term Radiation: {total_long_term_radiation} kJ/m^2")