import time
import spidev  # To handle SPI communication <--- only for Linux



# Set up SPI communication
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CS) 0
spi.max_speed_hz = 500000  # Max clock speed for the MAX6675

def read_temp():
    # Read 2 bytes of data from the sensor
    raw = spi.xfer2([0x00, 0x00])
    
    # Process the raw data
    value = (raw[0] << 8) | raw[1]  # Combine the two bytes into a single 16-bit value
    if value & 0x4:  # If the 3rd bit is set, there's an error (no thermocouple connected)
        return None
    temp_celsius = (value >> 3) * 0.25  # Remove lower 3 bits and convert to Celsius
    return temp_celsius

try:
    while True:
        temperature = read_temp()
        if temperature is not None:
            print(f"Temperature: {temperature:.2f} °C")
        else:
            print("Thermocouple not connected!")
        time.sleep(1)  # Wait 1 second before reading again
except KeyboardInterrupt:
    print("Program terminated")

# Close SPI communication when done
spi.close()
