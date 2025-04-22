extends Node
class_name Main

var load_data = {}
var save_data = {}
var load_path = "res://data/default.json"

# kart data
@onready var Capacity = $Battery/Capacity
@onready var Voltage = $Battery/Voltage
@onready var Scaling = $"Battery/Scaling Const"
@onready var Max_Speed = $"Kart Settings/Max Speed"
@onready var Acceleration = $"Kart Settings/Acceleration"
@onready var Weight = $"Kart Settings/Weight"
@onready var Friction = $"Kart Settings/Tire Friction Coeff"
@onready var Max_Speed_Unit = $"Kart Settings/Max Speed/OptionButton"
@onready var Acceleration_Unit = $"Kart Settings/Acceleration/OptionButton"
@onready var Weight_Unit = $"Kart Settings/Weight/OptionButton"
@onready var Capacity_Unit = $"Battery/Capacity/OptionButton"

# map scene
var map_scene: Map_Editor = preload("res://Scenes/map_edit.tscn").instantiate()
var map_loaded = false
var map_load = "res://data/data.json"

# save/load popup
@onready var file_popup = $FileDialog

# UI elements
@onready var profile_text = $Labels/Kart
@onready var path_text = $Labels/Map

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if !map_loaded:
		map_scene.visible = false
		get_tree().root.add_child(map_scene)
	#	map_scene.main_ref = self
		map_loaded = true

# given three points, gives the radius of the circle defined by them
func get_radius(x1, y1, x2, y2, x3, y3) -> int:
	var s1 = x1**2 + y1**2
	var s2 = x2**2 + y2**2
	var s3 = x3**2 + y3**2
	
	var m11 = x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)

	if m11 == 0:
		return float('inf')

	var m12 = s1*(y2 - y3) + s2*(y3 - y1) + s3*(y1 - y2)
	var m13 = s1*(x2 - x3) + s2*(x3 - x1) + s3*(x1 - x2)

	var x0 = 0.5 * m12 / m11
	var y0 = -0.5 * m13 / m11
	
	var radius = sqrt((x1 - x0)**2 + (y1 - y0)**2)
	return radius

func _on_run_pressed() -> void:
	## All conversions are exact
	
	var Q = Capacity.text.to_float()
	match Capacity_Unit.get_selected_id():
		0: # C is in ampere-hours, convert to coulombs
			Q *= 3600
		1: # coulombs, do nothing
			pass
	var V = Voltage.text.to_float()
	var scale = Scaling.text.to_float()
	
	var max_v = Max_Speed.text.to_float()
	match Max_Speed_Unit.get_selected_id():
		0: # velocity is in m/s, no conversion
			pass
		1: # kph
			max_v = (max_v*1000)/3600
		2: # ft/s
			max_v *= 0.3048
		3: # mph
			max_v = (max_v*(1/5280)*3600)*0.3048
	var max_a = Acceleration.text.to_float()
	match Acceleration_Unit.get_selected_id():
		0: # velocity is in m/s^2, no conversion
			pass
		1: # ft/s^2
			max_a *= 0.3048
	var friction_coeff = Friction.text.to_float()
	var cart_weight = Weight.text.to_float()
	match Weight_Unit.get_selected_id():
		0: # velocity is in kg, no change
			pass
		1: # grams
			cart_weight /= 1000
		2: # lbs
			cart_weight *= 0.45359237
			
	# get path data
	var pointList = Global.points
	
	## Setup Vars
	var radii = []
	var max_vs = []
	var ideal_vs = []
	var forces = []
	var work = []
	var power = []
	var times = []
	var charge = []
	var g = 9.8
	var drag_coeff = 0 # depricated, but maintained in case we want to reimplement
			
	## CALCULATE IDEAL VELOCITIES
	
	for i in range(len(pointList)):
		var x1 = []
		var x2 = pointList[i]
		var x3 = []
		if i == 0:
			x1 = pointList[-1]
			x3 = pointList[i+1]
		if i > 0 and i < len(pointList)-1:
			x1 = pointList[i-1]
			x3 = pointList[i+1]
		else:
			x1 = pointList[i-1]
			x3 = pointList[0]
			
		radii.append(get_radius(x1[0],x1[1],x2[0],x2[1],x3[0],x3[1]))

	# calculate max speeds by friction
	for each in radii:
		max_vs.append(sqrt(friction_coeff*g*each))

	# calculate max speeds with kart characteristics
	ideal_vs = max_vs
	for i in range(len(ideal_vs)):
		# starting point always velocity of 0
		if i == 0:
			ideal_vs[i] = 0
			continue

		# get adjacent points
		var v1 = ideal_vs[i-1]
		var x1 = pointList[i-1]
		var v2 = ideal_vs[i]
		var x2 = pointList[i]
		
		# check against max speed
		if v2 > max_v:
			ideal_vs[i] = max_v

		# check against max acceleration
		var dx = sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)
		
		if (v1*(v2-v1)/dx+((v2-v1)**2)/dx) > max_a:
			var t = (-v1+sqrt(v1**2+4*max_a*dx))/(2*max_a)
			ideal_vs[i] = v1+max_a*t
			times.append(t)
		else:
			var a = (v1*(v2-v1)/dx+((v2-v1)**2)/dx)
			var t = (-v1+sqrt(v1**2+4*a*dx))/(2*a)
			times.append(t)
			
	## CALCULATE ENERGY CONSUMPTION
	# calculate force on kart at each point
	for i in range(len(ideal_vs)):
		# assuming point spacing is sufficiently close so that acceleraton estimation can be over small time scale
		forces.append(drag_coeff*ideal_vs[i]**2+(ideal_vs[i] < max_v)*cart_weight*max_a)

	# calculate work done at each point since last point (left-sum)
	var totalDist = [0]
	var totalWork = [0]
	for i in range(len(forces)):
		var w = 0
		if i != 0:
			var x1 = pointList[i-1]
			var x2 = pointList[i]
			var dx = sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)
			totalDist.append(totalDist[i-1]+dx)
			w = forces[i]*dx
			totalWork.append(totalWork[i-1]+w)

		work.append(w)
		
	# P = W/t
	# I = P/V
	# Q = It
	# Q = W/V
	var total = 0
	for i in range(len(work)):
		var dQ = work[i]/V
		charge.append(dQ)
		total += dQ
		
	print(str(total)+" Coulombs, "+str(total/3600)+" Ampere-Hours")

######################################
#### FUNCTIONS TO OPEN MAP EDITOR ####
######################################

# open scene with no additional steps
func _on_new_map_pressed() -> void:
	map_scene.reset()
	launch_map()
	
# function caled when returning from map edit
func return_to_focus() -> void:
	self.visible = true
	map_scene.visible = false

func _on_edit_map_pressed() -> void:
	launch_map()

func launch_map():
	self.visible = false
	map_scene.visible = true

######################################
##### FUNCTIONS FOR FILE ACCESS ######
######################################

func _on_load_profile_pressed() -> void:
	file_popup.set_file_mode(FileDialog.FILE_MODE_OPEN_FILE) # select single file setting
	file_popup.clear_filters()
	file_popup.add_filter("*.json") # only look for json files
	file_popup.title = "Select a File"
	file_popup.popup_centered_ratio()
	
func _on_save_profile_pressed() -> void:
	file_popup.set_file_mode(FileDialog.FILE_MODE_SAVE_FILE) # Save File setting
	file_popup.clear_filters()
	# not sure if filters affect save functionality
	file_popup.add_filter("*.json") # only look for json files
	file_popup.title = "Select a Location"
	file_popup.popup_centered_ratio()
	
func _on_file_dialog_file_selected(path: String) -> void:
	if file_popup.get_file_mode() == 0: # if loading
		save_data = SaveManager.read_profile(path)
		
		# load each piece of data
		Capacity.text = str(save_data.capacity.value)
		Capacity_Unit.select(save_data.capacity.unit)
		
		Acceleration.text = str(save_data.acceleration.value)
		Acceleration_Unit.select(save_data.acceleration.unit)
		
		Weight.text = str(save_data.weight.value)
		Weight_Unit.select(save_data.weight.unit)
		
		Friction.text = str(save_data.friction.value)
		
		Max_Speed.text = str(save_data.max_speed.value)
		Max_Speed_Unit.select(save_data.max_speed.unit)
		
		Scaling.text = str(save_data.scaling.value)
		
		Voltage.text = str(save_data.voltage.value)
		
		# set file name in UI
		profile_text.text = "Profile: "+path.split("/")[-1]
		
	else: # if saving
		# store data
		load_data["acceleration"] = {"value": Acceleration.text.to_float(), "unit": Acceleration_Unit.get_selected_id()}
		load_data["capacity"] = {"value": Capacity.text.to_float(), "unit": Capacity_Unit.get_selected_id()}
		load_data["weight"] = {"value": Weight.text.to_float(), "unit": Weight_Unit.get_selected_id()}
		load_data["friction"] = {"value": Friction.text.to_float()}
		load_data["max_speed"] = {"value": Max_Speed.text.to_float(), "unit": Max_Speed_Unit.get_selected_id()}
		load_data["scaling"] = {"value": Acceleration.text.to_float()}
		load_data["voltage"] = {"value": Voltage.text.to_float()}
		
		# save file
		SaveManager.save_profile(path, load_data)
		
		# set file name in UI
		profile_text.text = "Profile: "+path.split("/")[-1]

######################################
######### DATA ENTRY HELPERS #########
######################################

func _on_tire_friction_coeff_text_changed(new_text: String) -> void:
	profile_change()

func _on_weight_text_changed(new_text: String) -> void:
	profile_change()

func _on_acceleration_text_changed(new_text: String) -> void:
	profile_change()

func _on_max_speed_text_changed(new_text: String) -> void:
	profile_change()

func _on_scaling_const_text_changed(new_text: String) -> void:
	profile_change()

func _on_cc_text_changed(new_text: String) -> void:
	profile_change()

func profile_change() -> void:
	if profile_text.text[-1] != "*":
		profile_text.text = profile_text.text + "*"
