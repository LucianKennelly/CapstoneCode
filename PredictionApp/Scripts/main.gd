extends Node
class_name Main

var data = preload("res://data/testNov8.csv")
var load_data = {}
var save_data = {}
var load_path = "res://data/default.json"
var CC
var Scaling
var Max_Speed
var Acceleration
var Weight
var Friction

# map scene
var map_scene: Map_Editor = preload("res://Scenes/map_edit.tscn").instantiate()
var map_loaded = false
var map_load = "res://data/data.json"
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	CC =  $Battery/CC
	Scaling = $"Battery/Scaling Const"
	Max_Speed =  $"Kart Settings/Max Speed"
	Acceleration = $"Kart Settings/Acceleration"
	Weight = $"Kart Settings/Weight"
	Friction = $"Kart Settings/Tire Friction Coeff"


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if !map_loaded:
		map_scene.visible = false
		get_tree().root.add_child(map_scene)
	#	map_scene.main_ref = self
		map_loaded = true


func _on_run_pressed() -> void:
	print(data.records[0]["time"])


func _on_load_pressed() -> void:
	save_data = SaveManager.read()
	CC.text = str(save_data.cc)
	Acceleration.text = str(save_data.acceleration)
	Weight.text = str(save_data.weight)
	Friction.text = str(save_data.friction)
	Max_Speed.text = str(save_data.max_speed)
	Scaling.text = str(save_data.scaling)
	print(save_data.cc)

func _on_tire_friction_coeff_text_changed(new_text: String) -> void:
	CC.text = new_text


func _on_weight_text_changed(new_text: String) -> void:
	Weight.text = new_text


func _on_acceleration_text_changed(new_text: String) -> void:
	Acceleration.text = new_text


func _on_max_speed_text_changed(new_text: String) -> void:
	Max_Speed.text = new_text


func _on_scaling_const_text_changed(new_text: String) -> void:
	Scaling.text = new_text


func _on_cc_text_changed(new_text: String) -> void:
	CC.text = new_text


func _on_save_pressed() -> void:
	load_data["acceleration"] = Acceleration.text.to_float()
	load_data["cc"] = CC.text.to_float()
	load_data["weight"] = Weight.text.to_float()
	load_data["friction"] = Friction.text.to_float()
	load_data["max_speed"] = Max_Speed.text.to_float()
	load_data["scaling"] = Scaling.text.to_float()
	#print(load_data)
	SaveManager.savef(load_data)


func _on_path_text_changed(new_text: String) -> void:
	SaveManager.load_path = new_text


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


func _on_load_profile_pressed() -> void:
#	SaveManager.path = load_path
	save_data = SaveManager.read()
	print(save_data)
	CC.text = str(save_data.cc)
	Acceleration.text = str(save_data.acceleration)
	Weight.text = str(save_data.weight)
	Friction.text = str(save_data.friction)
	Max_Speed.text = str(save_data.max_speed)
	Scaling.text = str(save_data.scaling)


func _on_profile_text_changed(new_text: String) -> void:
	load_path = new_text


func _on_save_profile_pressed() -> void:
#	SaveManager.path = load_path
#	SaveManager.create_new_save()
	load_data["acceleration"] = Acceleration.text.to_float()
	load_data["cc"] = CC.text.to_float()
	load_data["weight"] = Weight.text.to_float()
	load_data["friction"] = Friction.text.to_float()
	load_data["max_speed"] = Max_Speed.text.to_float()
	load_data["scaling"] = Scaling.text.to_float()
	SaveManager.savef(load_data)


func _on_map_text_changed(new_text: String) -> void:
	map_load = new_text
