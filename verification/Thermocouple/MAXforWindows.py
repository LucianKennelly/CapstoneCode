import time
import platform

# Mock SPI communication for Windows environment
class MockSPI:
    def open(self, bus, device):
        print(f"SPI mock: Opened bus {bus}, device {device}")
    
    def close(self):
        print("SPI mock: Closed SPI")

    def xfer2(self, data):
        print(f"SPI mock: Transferring data: {data}")
        # Simulating the response of a MAX6675 sensor with a random temperature value
        # The two bytes will simulate a temperature reading of around 25°C (which would be 100 in raw data)
        return [0x01, 0x90]  # Example response: 0x0190 -> 400 decimal -> 400 * 0.25 = 100°C

# Select the appropriate SPI library depending on the platform
if platform.system() == "Linux":
    import spidev
else:
    spidev = MockSPI()

# Function to read temperature from the (mock) MAX6675
def read_temp():
    # Open SPI bus and device
    spi = spidev.SpiDev()
    spi.open(0, 0)

    # Simulate reading 2 bytes from the sensor
    raw = spi.xfer2([0x00, 0x00])

    # Process the raw data (same as the real sensor logic)
    value = (raw[0] << 8) | raw[1]  # Combine the two bytes into a single 16-bit value
    if value & 0x4:  # If the 3rd bit is set, there's an error (e.g., no thermocouple connected)
        spi.close()
        return None

    # Convert the raw value to Celsius temperature (remove lower 3 bits and multiply by 0.25)
    temp_celsius = (value >> 3) * 0.25
    spi.close()
    return temp_celsius

# Main loop to continuously read temperature
try:
    while True:
        temperature = read_temp()
        if temperature is not None:
            print(f"Temperature: {temperature:.2f} °C")
        else:
            print("Thermocouple not connected or error!")
        time.sleep(1)  # Wait 1 second before reading again

except KeyboardInterrupt:
    print("Program terminated.")
