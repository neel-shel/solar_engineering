from datetime import datetime, timedelta
import numpy as np

def days_from_jan(input_date):
    current_year = datetime.now().year
    date = datetime.strptime(f"{input_date} {current_year}", "%b %d %Y")
    jan_1 = datetime(year=current_year, month=1, day=1)
    delta = date - jan_1
    return delta.days + 1  # Include Jan 1 as day 1

class SolarParameters:
    def __init__(self, n, latitude, longitude, LST, l_st):
        self.n = n
        self.latitude = latitude
        self.longitude = longitude
        self.LST = LST  # Local Standard Time (used for calculating solar time)
        self.l_st = l_st  # Local Standard Meridian (used for offset)

        # Calculate solar parameters
        self.delta_s = self.solar_declination()
        self.ET = self.equation_of_time()
        self.ST = self.solar_time()
        self.h_s = self.hour_angle()
        self.alpha = self.solar_attitude()
        self.z = self.solar_zenith_angle()
        self.h_ss, self.h_sr = self.sunset_and_sunrise_times()
        
        # print(f"Sunset Time (Solar Time): {self.h_ss}, Sunrise Time (Solar Time): {self.h_sr}")

        # Convert Solar Time to Local Time
        self.h_ss_local, self.h_sr_local = self.convert_solar_to_local_time(self.h_ss), self.convert_solar_to_local_time(self.h_sr)

        # Print all solar parameters
        print(f"Solar Declination (delta_s): {self.delta_s}°")
        print(f"Equation of Time (ET): {self.ET} minutes")
        print(f"Solar Time (ST): {self.ST}")
        print(f"Hour Angle (h_s): {self.h_s}°")
        print(f"Solar Attitude (alpha): {self.alpha}°")
        print(f"Solar Zenith Angle (z): {self.z}°")

        print(f"Sunset Time (Local Time): {self.h_ss_local}, Sunrise Time (Local Time): {self.h_sr_local}")

    def solar_declination(self):
        delta_s = np.degrees(np.arcsin(np.sin(np.radians(23.45)) * np.sin(np.radians(360 * (284 + self.n) / 365))))
        return delta_s
    
    def equation_of_time(self):
        B = 360 * (self.n - 81) / 364
        ET = 9.87 * np.sin(np.radians(2 * B)) - 7.53 * np.cos(np.radians(B)) - 1.5 * np.sin(np.radians(B))
        return ET
    
    def solar_time(self):
        ST = self.process_solar_time(self.LST, self.ET + (self.l_st - self.longitude) * 4)
        return ST
    
    def hour_angle(self):
        h_s = 15 * self.hours_from_solar_noon(self.ST)
        return h_s
    
    def solar_attitude(self):
        alpha = np.degrees(np.arcsin(np.sin(np.radians(self.latitude)) * np.sin(np.radians(self.delta_s)) + np.cos(np.radians(self.latitude)) * np.cos(np.radians(self.delta_s)) * np.cos(np.radians(self.h_s))))
        return alpha
    
    def solar_zenith_angle(self):
        zenith_angle = 90 - self.alpha
        return zenith_angle
    
    def sunset_and_sunrise_times(self):
        temp = np.degrees(np.arccos(-np.tan(np.radians(self.latitude)) * np.tan(np.radians(self.delta_s))))
        h_ss = self.process_sunset_and_sunrise_times(temp)  # Sunset time in minutes from solar noon
        h_sr = self.process_sunset_and_sunrise_times(-temp)  # Sunrise time in minutes from solar noon
        solar_noon = datetime.strptime("12:00:00", "%H:%M:%S")
        sunset_time = solar_noon + timedelta(minutes=h_ss)
        sunrise_time = solar_noon + timedelta(minutes=h_sr)
        return sunset_time.strftime("%H:%M:%S"), sunrise_time.strftime("%H:%M:%S")

    def process_sunset_and_sunrise_times(self, temp):
        minutes = (temp / 15) * 60  # 15 degrees corresponds to 1 hour (60 minutes)
        return minutes

    def convert_solar_to_local_time(self, solar_time_str):
        # Convert Solar Time back to Local Time
        solar_time = datetime.strptime(solar_time_str, "%H:%M:%S")
        
        # Calculate the time difference due to the longitude offset
        longitude_offset_minutes = (self.l_st - self.longitude) * 4  # 1 degree of longitude = 4 minutes
        local_time = solar_time + timedelta(minutes=longitude_offset_minutes-self.ET)
        
        return local_time.strftime("%H:%M:%S")
    
    def process_solar_time(self, lst_time_str, minutes_to_add):
        lst_time = datetime.strptime(lst_time_str, "%Y-%m-%d %H:%M:%S")
        unix_timestamp = int(lst_time.timestamp())
        new_timestamp = unix_timestamp + (minutes_to_add * 60)
        new_time = datetime.fromtimestamp(new_timestamp)
        new_time_str = new_time.strftime("%Y-%m-%d %H:%M:%S")
        return new_time_str

    def hours_from_solar_noon(self, time_str):
        solar_noon_str = "12:00:00"
        time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        solar_noon = datetime.strptime(solar_noon_str, "%H:%M:%S")
        time_diff = time - solar_noon
        hours_diff = time_diff.total_seconds() / 3600  # Convert seconds to hours
        return hours_diff

if __name__ == "__main__":
    input_date = "Feb 1"
    n = days_from_jan(input_date)
    
    # Example coordinates for Gainesville, Florida
    latitude = 29.68
    longitude = -82.27
    
    # Local Standard Meridian (LST) is typically a multiple of 15 degrees, for example 75°W for Eastern Standard Time
    l_st = -75  # Local Standard Meridian (EST is 75°W, meaning UTC-5)
    
    # Example Local Standard Time (LST) (format "YYYY-MM-DD HH:MM:SS")
    LST = "2025-02-01 5:00:00"
    
    solar_parameters = SolarParameters(n, latitude, longitude, LST, l_st)
