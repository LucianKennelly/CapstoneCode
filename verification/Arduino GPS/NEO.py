import serial
import pynmea2

# Open serial connection to NEO-6M GPS Module
# Make sure the port matches the one your device is connected to (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

# Continuously read data from the GPS module
while True:
    try:
        line = ser.readline().decode('ascii', errors='replace')  # Read a line of NMEA data
        if line.startswith('$GPGGA'):  # Check for GPGGA sentence, which provides fix data
            msg = pynmea2.parse(line)  # Parse the NMEA sentence
            print(f"Timestamp: {msg.timestamp}")
            print(f"Latitude: {msg.latitude} {msg.lat_dir}")
            print(f"Longitude: {msg.longitude} {msg.lon_dir}")
            print(f"Altitude: {msg.altitude} {msg.altitude_units}")
            print(f"Number of Satellites: {msg.num_sats}")
            print(f"Fix Quality: {msg.gps_qual}")  # 0 = Invalid, 1 = GPS fix, 2 = DGPS fix
            print('-' * 40)
    except pynmea2.ParseError as e:
        print(f"Error parsing NMEA data: {e}")
    except KeyboardInterrupt:
        print("Exiting program")
        break

# Close the serial connection when done
ser.close()
