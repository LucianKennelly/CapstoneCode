# EVGP Battery Drain Simulator

## Description
The EVGP Battery Drain Simulator is a tool designed to predict electric vehicle (EV) battery drain. It uses input data such as position, current, and voltage, along with the characteristics of the battery and kart, to run a prediction algorithm. The simulator estimates the energy consumed and converts this into a battery percentage, providing a comprehensive output to the user.

The project includes a graphical user interface (GUI) that allows users to interact with the simulation by adjusting parameters such as vehicle mass and observing the battery drain behavior through real-time visualization.

## Installation
To set up the EVGP Battery Drain Simulator, follow these steps:

* Clone the repository to your local machine.
* Install the required dependencies using pip:
    `pip3 install -r /path/to/requirements.txt`

## Usage
Prepare your input data, ensuring it includes parameters like position, current, voltage, and battery characteristics.
Run the simulation program to predict battery drain.
View the output data, which will detail the estimated battery consumption.

To run and navigate the GUI, follow these steps:
* Using the command prompt, navigate to the `path/to/verification` folder.
* Type `python gui.py`
* Use the mass slider to adjust the mass of the kart (0 - 2000 kg).
* Click "Run Test" to update the visualization.
* View the graph displaying state of charge vs. time.
* Observe power consumption updates in the Tkinter window.

## Dependencies
Python 3.12.7
Any additional libraries specified in requirements.txt
