extends Node
class_name Main

var load_data = {}
var save_data = {}
var load_path = "res://data/default.json"

# kart data
@onready var Capacity = $Battery/Capacity
@onready var Scaling = $"Battery/Scaling Const"
@onready var Max_Speed = $"Kart Settings/Max Speed"
@onready var Acceleration = $"Kart Settings/Acceleration"
@onready var Weight = $"Kart Settings/Weight"
@onready var Friction = $"Kart Settings/Tire Friction Coeff"
@onready var Max_Speed_Unit = $"Kart Settings/Max Speed/OptionButton"
@onready var Acceleration_Unit = $"Kart Settings/Acceleration/OptionButton"
@onready var Weight_Unit = $"Kart Settings/Weight/OptionButton"
@onready var Capacity_Unit = $"Battery/Capacity/OptionButton"

# prediction cosntants
var SOC: float
var Q
var I
var t

# map scene
var map_scene: Map_Editor = preload("res://Scenes/map_edit.tscn").instantiate()
var map_loaded = false
var map_load = "res://data/data.json"

# save/load popup
@onready var file_popup = $FileDialog

# UI elements
@onready var profile_text = $Labels/Kart
@onready var path_text = $Labels/Map

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	SOC = float(Capacity.text)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if !map_loaded:
		map_scene.visible = false
		get_tree().root.add_child(map_scene)
	#	map_scene.main_ref = self
		map_loaded = true


func _on_run_pressed() -> void:
	var C = 1.099 # C battery capacity
	var I_avg = 26.1 # A
	var V_avg = 11.93 # V
	Q = 3.19 # aH
	SOC = float(Capacity.text)
	for point in Global.points:
		#print(SOC)
		if (point.x == 0):
			t = 0
		else:
			t = float(Max_Speed.text)/sqrt(pow(point.x,2) + pow(point.y,2)) # delta time
		print("time:"+str(t))
		print(-t/(C*(V_avg/I_avg)))
		I = float(7*pow(exp(1),float(-t/(C*(V_avg/I_avg)))))
		SOC = SOC + (1/Q)*(-I) # coulomb count change
		$Meta/Output.text = str((float(Capacity.text)-SOC)) + "%"
		break
	pass

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
