import glob
import time

# Locate sensor file
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]  # Automatically finds sensor
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    
    temp_output = lines[1].split("t=")
    if len(temp_output) > 1:
        temp_c = float(temp_output[1]) / 1000.0  # Convert millidegrees to Celsius
        temp_f = (temp_c * 9/5) + 32  # Convert Celsius to Fahrenheit
        return temp_f  # Return only Fahrenheit
    return None

if __name__ == "__main__":
    while True:
        temp_f = read_temp()
        print("Temperature: {:.2f}°F".format(temp_f))
        time.sleep(2)
