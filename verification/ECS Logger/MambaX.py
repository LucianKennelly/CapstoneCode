import RPi.GPIO as GPIO
import time

# Define the GPIO pin connected to the ESC's signal input
ESC_PIN = 18  # GPIO Pin for PWM signal (BCM numbering)
PWM_FREQUENCY = 50  # Standard frequency for servo/ESC PWM (50Hz)

GPIO.setmode(GPIO.BCM)  # Set GPIO to BCM numbering
GPIO.setup(ESC_PIN, GPIO.OUT)

# Initialize PWM on the ESC pin at 50Hz
pwm = GPIO.PWM(ESC_PIN, PWM_FREQUENCY)
pwm.start(0)  # Start PWM with 0% duty cycle (motor off)

# Helper function to control the ESC
def set_throttle(duty_cycle):
    pwm.ChangeDutyCycle(duty_cycle)

try:
    while True:
        # Example: Increase throttle gradually
        for duty_cycle in range(5, 10):  # 5-10% duty cycle corresponds to low throttle
            set_throttle(duty_cycle)
            time.sleep(1)

        # Hold for a few seconds
        time.sleep(3)

        # Example: Stop the motor
        set_throttle(0)  # Set duty cycle to 0% (motor off)
        time.sleep(3)

except KeyboardInterrupt:
    print("Program interrupted, stopping motor.")
    pwm.stop()  # Stop the PWM output
    GPIO.cleanup()  # Cleanup GPIO settings

