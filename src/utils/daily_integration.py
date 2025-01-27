import numpy as np

class DailyIntegration:
    def __init__(self, L, delta_s, h_s, h_ss, H_bar_h, extraterrestrial_radiation_factor, E_sc=1367, w_s=1.06*np.pi/180):
        # Initialize parameters
        self.L = L
        self.delta_s = delta_s
        self.h_s = h_s
        self.h_ss = h_ss
        self.h_ss_rad = np.radians(h_ss)
        self.H_bar_h = H_bar_h
        self.S0 = 24/np.pi*self.h_ss_rad
        self.E_sc = E_sc
        self.extraterrestrial_radiation_factor = extraterrestrial_radiation_factor

        print(f"Initialized parameters:\n L: {self.L}, delta_s: {self.delta_s}, h_s: {self.h_s}, h_ss: {self.h_ss}")
        print(f"h_ss_rad: {self.h_ss_rad}, H_bar_h: {self.H_bar_h}, S0: {self.S0}, E_sc: {self.E_sc}, extraterrestrial_radiation_factor: {self.extraterrestrial_radiation_factor}")

        self.h_s_rad = np.radians(self.h_s)
        self.h_ss_rad = np.radians(self.h_ss)

        # Calculate r_d
        self.r_d = self.hourly_diffuse_to_average_daily_diffuse_radiation()
        print(f"r_d (hourly diffuse to average daily diffuse radiation): {self.r_d}")

        # Calculate q
        self.q = np.cos(np.radians(self.L)) * np.cos(np.radians(self.delta_s))
        print(f"q: {self.q}")

        # Calculate A
        self.A = np.sin(self.h_ss_rad) - self.h_ss_rad * np.cos(self.h_ss_rad)
        print(f"A: {self.A}")

        # Calculate h0 and h0_deg
        self.h0 = np.arcsin(self.q * self.A / self.h_ss_rad)
        self.h0_deg = np.degrees(self.h0)
        print(f"h0 (radians): {self.h0}, h0_deg (degrees): {self.h0_deg}")

        # Calculate H0
        self.H0 = 24/np.pi * self.h_ss_rad * self.extraterrestrial_radiation_factor * self.E_sc * np.sin(self.h0)
        print(f"H0 (radiation factor): {self.H0}")

        # Calculate K_t
        self.K_t = H_bar_h / self.H0
        print(f"K_t (clearness index): {self.K_t}")

        # Calculate a1 and a2
        self.a1 = 0.41341 * self.K_t + 0.61197 * self.K_t**2 - 0.01886 * self.K_t * self.S0 + 0.00759 * self.S0
        self.a2 = max(0.054, 0.28116 + 2.2475 * self.K_t - 1.7611 * self.K_t**2 - 1.84535 * np.sin(self.h0) + 1.681 * np.square(np.sin(self.h0)))
        print(f"a1: {self.a1}, a2: {self.a2}")

        # Calculate atmospheric extinction coefficient
        self.atmospheric_extinction_coefficient = self.a2 / self.a1
        print(f"Atmospheric extinction coefficient: {self.atmospheric_extinction_coefficient}")

        # Calculate B
        self.B = (0.5 + np.square(np.cos(self.h_ss_rad))) * w_s - 0.75 * np.sin(2 * self.h_ss_rad)
        print(f"B (adjusted factor): {self.B}")

        # Calculate r_t
        self.r_t = self.hourly_total_to_average_daily_diffuse_radiation()
        print(f"r_t (hourly total to average daily diffuse radiation): {self.r_t}")

    def hourly_diffuse_to_average_daily_diffuse_radiation(self):
        print("Calculating hourly diffuse to average daily diffuse radiation...")
        result = np.pi / 24 * np.divide((np.cos(self.h_s_rad) - np.cos(self.h_ss_rad)),
                                        (np.sin(self.h_ss_rad) - np.pi / 180 * self.h_ss * np.cos(self.h_ss_rad)))
        print(f"Result of hourly diffuse to average daily diffuse radiation: {result}")
        return result

    def hourly_total_to_average_daily_diffuse_radiation(self):
        print("Calculating hourly total to average daily diffuse radiation...")
        result = self.r_d * ((1 + self.q * self.A * self.atmospheric_extinction_coefficient * self.r_d * 24 / np.pi) /
                             ((1 + self.q * self.atmospheric_extinction_coefficient * self.B / self.A * 24 / np.pi)))
        print(f"Result of hourly total to average daily diffuse radiation: {result}")
        return result
