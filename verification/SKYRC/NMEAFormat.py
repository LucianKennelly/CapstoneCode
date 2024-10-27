import pynmea2

# Load and parse NMEA sentences
with open('path_to_your_data_file.nmea', 'r') as nmea_file:
    for line in nmea_file:
        try:
            msg = pynmea2.parse(line)
            print(f'Timestamp: {msg.timestamp}, Latitude: {msg.latitude}, Longitude: {msg.longitude}')
        except pynmea2.ParseError as e:
            print(f"Error parsing line: {line} -> {e}")
