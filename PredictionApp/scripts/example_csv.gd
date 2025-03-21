extends Node
var data = preload("res://data/testNov8.csv")
var load_data = {}
var save_data
var load_path
var CC
var Scaling
var Max_Speed
var Acceleration
var Weight
var Friction

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
	pass


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
	print(load_data)
	SaveManager.savef(load_data)


func _on_path_text_changed(new_text: String) -> void:
	SaveManager.load_path = new_text
