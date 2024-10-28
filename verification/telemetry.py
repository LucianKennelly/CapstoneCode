import time
from time import sleep
from pyembedded.rasberry_pi_tools.raspberrypi import PI
# Need to install in terminal pip3 install pyembedded
PyP110 = PI()

p110 = PyP110.P110("%s",PyP110.get_connected_ip_addr(newtork='wlan0')), "kennelly25@up.edu", "********" #Creating a P110 plug object

p110.handshake() #Creates the cookies required for further methods
p110.login() #Sends credentials to the plug and creates AES Key and IV for further methods


data = p110.getEnergyUsage()
print(data)

with open("p110.csv", "a", ) as f:
    f.write("Energy Usage: %s", str(data))
    f.write('\n')
    f.close()