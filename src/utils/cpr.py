import numpy as np

class CPR:
    def __init__(self, h_s, h_ss):
        print(f"Initializing CPR with h_s: {h_s}, h_ss: {h_ss}")
        
        self.h_s = h_s
        self.h_ss = h_ss

        # Convert angles to radians
        self.h_s_rad = np.radians(self.h_s)
        self.h_ss_rad = np.radians(self.h_ss)
        
        print(f"Converted h_s to radians: {self.h_s_rad}")
        print(f"Converted h_ss to radians: {self.h_ss_rad}")

        # Calculate r_d and r_t
        self.r_d = self.hourly_diffuse_to_average_daily_diffuse_radiation()
        print(f"Diffuse radiation (r_d): {self.r_d}")
        
        self.r_t = self.hourly_total_to_average_daily_diffuse_radiation()
        print(f"Total diffuse radiation (r_t): {self.r_t}")

    def hourly_diffuse_to_average_daily_diffuse_radiation(self):
        print("Calculating hourly diffuse to average daily diffuse radiation...")
        
        numerator = np.cos(self.h_s_rad) - np.cos(self.h_ss_rad)
        denominator = np.sin(self.h_ss_rad) - np.pi / 180 * self.h_ss * np.cos(self.h_ss_rad)
        
        print(f"Numerator (cos(h_s) - cos(h_ss)): {numerator}")
        print(f"Denominator (sin(h_ss) - pi/180*h_ss*cos(h_ss)): {denominator}")
        
        r_d = (np.pi / 24) * np.divide(numerator, denominator)
        print(f"Resulting r_d: {r_d}")
        
        return r_d
    
    def hourly_total_to_average_daily_diffuse_radiation(self):
        print("Calculating hourly total to average daily diffuse radiation...")
        
        # Coefficients for the calculation
        a0 = 0.409
        a1 = 0.5019
        a = a0 + a1 * np.sin(np.radians(self.h_ss - 60))
        print(f"Calculated 'a': {a}")
        
        b0 = 0.6609
        b1 = 0.4767
        b = b0 + b1 * np.sin(np.radians(self.h_ss - 60))
        print(f"Calculated 'b': {b}")
        
        # Calculate r_t
        r_t = (a + b * np.cos(np.radians(self.h_s))) * self.r_d
        print(f"Calculated total diffuse radiation (r_t): {r_t}")
        
        return r_t

# Example usage (you can test it like this)
if __name__ == "__main__":
    h_s = 30  # Example solar hour angle
    h_ss = 60  # Example solar noon hour angle
    
    cpr = CPR(h_s, h_ss)
    print(f"Diffuse radiation (r_d): {cpr.r_d}")
    print(f"Total diffuse radiation (r_t): {cpr.r_t}")
