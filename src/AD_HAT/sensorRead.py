import time
import ADS1263
import RPi.GPIO as GPIO
import numpy as np
from ds18b20_read import read_temp  # Import temperature reading function
import atexit  # Ensure GPIO cleanup on exit
import numpy as np

class SensorReader:
    REF = 5.07  # Modify according to actual voltage
    
    # Mapping channels to sensor names and units
    SENSOR_INFO = {
        0: {"name": "Turbidity", "unit": "NTU"},
        1: {"name": "TDS", "unit": "ppm"},
        2: {"name": "pH", "unit": ""}
    }
    SENSOR_INFO = {
                "Turbidity": {"unit": "NTU"},
                "TDS": {"unit": "ppm"},
                "pH": {"unit": ""},
                "Temperature": {"unit": "°F"}
            }
    
    STABILITY_THRESHOLDS = {
        "Turbidity": 0.10,  # 10% variation allowed
        "TDS": 0.07,  # 7% variation allowed
        "pH": 0.03,  # 3% variation for better accuracy
    }
    
    def __init__(self):

        atexit.register(self.cleanup_gpio)  # Register the cleanup function
        try:
            ADC = ADS1263.ADS1263()
            if ADC.ADS1263_init_ADC1('ADS1263_400SPS') == -1:
                exit()
            ADC.ADS1263_SetMode(0)

            results = {}

            # # Step 1: Temperature Measurement
            # results["Temperature"] = get_temperature()
            # input("\nPress Enter to continue to Turbidity testing...")
            
            # # Step 2-4: Turbidity, TDS, and pH calibration
            # results["Turbidity"] = get_stable_reading(0, turbidity_voltage_to_ntu)
            # input("\nPress Enter to continue to TDS testing...")
            # results["TDS"] = get_stable_reading(1, tds_voltage_to_ppm, read_temp)
            # input("\nPress Enter to continue to pH testing...")
                

            # # pH Calibration
            # ph_coeffs = calibrate_ph()
            # results["pH"] = measure_ph(ph_coeffs)

            # # Display Final Results
            # print("\nFinal Sensor Readings:")
            # for key, value in results.items():
            #     print(f"{key}: {value:.2f} {SENSOR_INFO.get(key, {}).get('unit', '')}")


            # print("\nData collection completed.")

        except IOError as e:
            print(e)
        except KeyboardInterrupt:
            print("\nctrl + c: Program end")
            ADC.ADS1263_Exit()
            exit()


        # Initializing active variables 
        self.active_temp = None
        self.active_ph = None 
        self.active_turbidity = None
        self.active_tds = None 

    def haylie_test(self):
        print("WE HAVE A CLASS SETUP NOW")

    # Ensure GPIO is cleaned up when the script exits
    def cleanup_gpio(self):
        GPIO.cleanup()


    def turbidity_voltage_to_ntu(self, voltage):
        """Convert voltage from turbidity sensor to NTU."""
        if voltage is None:
            return None  # Handle NoneType input gracefully

        print(f"Raw voltage: {voltage:.4f} V")

        if voltage > 5:
            return 0  # Above lager reference point
        elif voltage < 0.06:
            return 4000  # Below whole milk reference point
        elif voltage <= 1.45:
            ntu_value = -2294.711 * voltage + 3743.243
        elif voltage <= 4.15:
            ntu_value = -157.0281 * voltage + 668.5181
        else:  # voltage > 4.15 and <= 5
            ntu_value = -17.4179 * voltage + 82.30954927

        return max(ntu_value, 0)  # Ensure NTU is never negative



    def tds_voltage_to_ppm(self, voltage, temperature):
        """Convert voltage from TDS sensor to ppm with temperature compensation."""

        # Convert temperature from °F to °C
        to_celsius = (temperature - 32) * 5.0 / 9.0

        # Temperature compensation
        compensation_coefficient = 1.0 + 0.02 * (to_celsius - 25.0)
        compensated_voltage = voltage / compensation_coefficient

        # For troubleshooting
        print(f"Raw voltage: {voltage:.4f} V")

        # New linear curve fit based on collected data
        tds_value = 3688.5* compensated_voltage -442.62

        return max(tds_value, 0)  # Ensure no negative values



    def get_temperature(self):
        """
        Reads temperature every 2 seconds for 10 seconds and returns the average.
        """
        print("\nStep 1: Place temperature probe in water.")
        input("Press Enter when the probe is in the water...")
        print(f"\nGetting stable temperature reading...")

        temp_readings = []
        start_time = time.time()

        while (time.time() - start_time) < 10:
            temp = read_temp()
            temp_readings.append(temp)
            print(f"Reading: {temp:.1f}°F")
            time.sleep(2)

        avg_temp = sum(temp_readings) / len(temp_readings)
        print(f"\nAverage Temperature: {avg_temp:.1f}°F")
        return avg_temp

    

    def get_stable_reading(self, channel, conversion_func=None, temp_func=None):
        print(f"\nStep {channel + 2}: Place {self.SENSOR_INFO[channel]['name']} sensor in water.")
        input("Press Enter when the sensor is in the water...")
        print(f"\nGetting stable reading for {self.SENSOR_INFO[channel]['name']}...")

        readings = []
        start_time = time.time()
        stable = False

        while (time.time() - start_time) < 10:
            sample_readings = []
            sample_start = time.time()

            self.ADC.ADS1263_SetChannel(8)  # Force ADC to read GND before switching
            time.sleep(1)

            self.ADC.ADS1263_SetChannel(channel)
            self.ADC.ADS1263_WaitDRDY()

            while (time.time() - sample_start) < 2:  # Collect data for 2 seconds
                voltage = self.ADC.ADS1263_Read_ADC_Data() * self.REF / 0x7FFFFFFF

                if temp_func:
                    temperature = temp_func()
                    reading = conversion_func(voltage, temperature)
                else:
                    reading = conversion_func(voltage) if conversion_func else voltage

                sample_readings.append(reading)
                time.sleep(0.25)  # Faster sampling (optional)

            avg_sampled_reading = sum(sample_readings) / len(sample_readings)
            readings.append(avg_sampled_reading)
            print(f"Reading: {avg_sampled_reading:.2f} {self.SENSOR_INFO[channel]['unit']}")

            if len(readings) > 5:  # Use last 5 readings for stability
                avg = sum(readings[-5:]) / 5
                threshold = self.STABILITY_THRESHOLDS[self.SENSOR_INFO[channel]['name']]
                if all(abs(r - avg) / avg < threshold for r in readings[-5:]):
                    stable = True
                    break

        avg_reading = sum(readings) / len(readings)
        print(f"\nStable {self.SENSOR_INFO[channel]['name']} Reading: {avg_reading:.2f} {self.SENSOR_INFO[channel]['unit']}")
        return avg_reading

    def calibrate_ph(self):
        """
        Calibrates the pH sensor using known pH 4.00, 7.00, and 10.01 buffer solutions.
        Returns the coefficients of the calibration curve.
        """

        # Fun explanation for kids about calibration
        print("""
    For the last sensor, we need to calibrate it!  

    📏 What is Calibration?  
    It's like teaching the sensor the **correct answers** so it doesn’t guess wrong!

    💡 Why do we need it?  
    If we don’t **train** the sensor, it might **think lemonade is water!** 🍋💦  
    We use **special pH solutions (4, 7, and 10)** to help it **learn!** 🧪
        """)
        
        input("Press Enter to start the calibration process...")

        ph_values = [4.00, 7.00, 10.01]  # Calibration reference points
        voltage_readings = []

        for ph in ph_values:
            print(f"\nPlace pH probe in {ph:.2f} buffer solution.")
            input("Press Enter when the probe is in the solution...")

            readings = []
            start_time = time.time()
            stable = False  # Added stability check

            while (time.time() - start_time) < 10:
                sample_readings = []
                sample_start = time.time()

                # ✅ **Force ADC to read from GND (channel 8) first**
                self.ADC.ADS1263_SetChannel(8)  # Set ADC to GND to clear floating voltage
                time.sleep(1)  # Allow time to stabilize

                # ✅ **Now switch to the pH sensor channel (channel 2)**
                self.ADC.ADS1263_SetChannel(2)
                self.ADC.ADS1263_WaitDRDY()

                while (time.time() - sample_start) < 2:
                    voltage = self.ADC.ADS1263_Read_ADC_Data() * self.REF / 0x7FFFFFFF
                    sample_readings.append(voltage)
                    print(f"Raw pH Voltage: {voltage:.4f} V")
                    time.sleep(0.5)

                avg_sampled_voltage = sum(sample_readings) / len(sample_readings)
                readings.append(avg_sampled_voltage)

                # ✅ **Apply the 5-reading stability check with a 3% threshold**
                if len(readings) > 5:
                    avg = sum(readings[-5:]) / 5  # Use last 5 readings
                    if all(abs(r - avg) / avg < 0.03 for r in readings[-5:]):  # Stricter 3% threshold
                        stable = True
                        break

            avg_voltage = sum(readings) / len(readings)
            voltage_readings.append(avg_voltage)
            print(f"\nStable pH {ph:.2f} Voltage: {avg_voltage:.6f} V")

            input("Remove the probe, clean it, and press Enter when ready...")

        # Use linear fit (1st-degree polynomial) since we now have 3 points
        coefficients = np.polyfit(voltage_readings, ph_values, 1)  
        
        print("\nCalibration Complete! Curve fit generated:")
        print(f"pH = {coefficients[0]:.1f} * Voltage + {coefficients[1]:.1f}")

        return coefficients  # Returns the coefficients for linear fit


    def measure_ph(self, coefficients):
        """
        Uses the calibrated coefficients to measure and compute pH.
        """
        print("\nStep 5: Place pH probe in water sample.")
        input("Press Enter when the probe is in the water...")

        readings = []
        start_time = time.time()
        stable = False

        while (time.time() - start_time) < 10:
            sample_readings = []
            sample_start = time.time()

            # ✅ **Force ADC to read from GND (channel 8) first**
            self.ADC.ADS1263_SetChannel(8)  # Set ADC to GND to clear floating voltage
            time.sleep(1)  # Allow time to stabilize
            
            # ✅ **Now switch to the pH sensor channel (channel 2)**
            self.ADC.ADS1263_SetChannel(2)
            self.ADC.ADS1263_WaitDRDY()

            while (time.time() - sample_start) < 2:
                voltage = self.ADC.ADS1263_Read_ADC_Data() * self.REF / 0x7FFFFFFF
                pH_value = coefficients[0] * voltage + coefficients[1]
                sample_readings.append(pH_value)
                time.sleep(0.5)

            avg_sampled_pH = sum(sample_readings) / len(sample_readings)
            readings.append(avg_sampled_pH)
            print(f"Raw pH Value: {avg_sampled_pH:.2f}")

            # ✅ **Apply the 5-reading stability check with a 3% threshold**
            if len(readings) > 5:
                avg = sum(readings[-5:]) / 5  # Use last 5 readings
                if all(abs(r - avg) / avg < 0.03 for r in readings[-5:]):  # Stricter 3% threshold
                    stable = True
                    break

        avg_pH = sum(readings) / len(readings)
        print(f"\nStable pH Reading: {avg_pH:.2f}")
        
        input("Remove the probe, clean it, and press Enter when ready...")
        return avg_pH


    